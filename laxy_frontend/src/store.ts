// import * as _ from 'lodash';
import filter from 'lodash-es/filter';
import pick from 'lodash-es/pick';
import cloneDeep from 'lodash-es/cloneDeep';
import update from 'lodash-es/update';
import head from 'lodash-es/head';

import Vuex from 'vuex';
import Vue from 'Vue';
import axios, {AxiosResponse} from 'axios';
import {ComputeJob, LaxyFile, Sample, SampleSet} from './model';
import {WebAPI} from './web-api';

export const SET_USER_PROFILE = 'set_user_profile';
export const ADD_SAMPLES = 'add_samples';
export const SET_SAMPLES = 'set_samples';
export const SET_SAMPLES_ID = 'set_samples_id';
export const SET_PIPELINE_PARAMS = 'set_pipeline_params';
export const SET_PIPELINE_DESCRIPTION = 'set_pipeline_description';
export const SET_JOBS = 'set_jobs';
export const SET_FILESET = 'set_fileset';
export const SET_VIEWED_JOB = 'set_viewed_job';

export const FETCH_USER_PROFILE = 'fetch_user_profile';
export const FETCH_JOBS = 'fetch_jobs';
export const FETCH_FILESET = 'fetch_fileset';
export const FETCH_JOB = 'fetch_job';

interface JobsPage {
    total: number;  // total number of jobs on all pages
    jobs: ComputeJob[];    // jobs for just the page we've retrieved
}

export const Store = new Vuex.Store({
    strict: true,
    state: {
        user_profile: {},
        samples: new SampleSet(),
        pipelineParams: {
            reference_genome: 'hg19',
            description: '',
        },
        jobs: {total: 0, jobs: [] as ComputeJob[]} as JobsPage,
        filesets: {} as { [key: string]: LaxyFileSet },
        currentViewedJob: {} as ComputeJob,
    },
    getters: {
        samples: state => {
            return state.samples;
        },
        pipelineParams: state => {
            return state.pipelineParams;
        },
        sample_cart_count: state => {
            if (state.samples.items != undefined) {
                return state.samples.items.length;
            }
            return 0;
        },
        jobs: state => {
            return state.jobs;
        },
        currentJobFiles: (state, getters) => {
            const job = state.currentViewedJob;
            if (!job) {
                return [];
            }
            const getFileset = getters.fileset;
            const infileset = getFileset(job.input_fileset_id);
            const outfileset = getFileset(job.output_fileset_id);
            const filez = [];
            filez.push(...(infileset && infileset.files || []));
            filez.push(...(outfileset && outfileset.files || []));
            return filez;
        },
        // Call like: this.$store.getters.fileset('SomeBlafooLongId')
        fileset: state => {
            return (fileset_id: string) => {
                return state.filesets[fileset_id];
            };
        },
        filesets: state => {
            return state.filesets;
        },
        // currentInputFileset: (state, getters) => {
        //     return state.filesets[(state.currentViewedJob as any).input_fileset_id];
        // },
        // currentOutputFileset: (state, getters) => {
        //     return state.filesets[(state.currentViewedJob as any).output_fileset_id];
        // },
        fileById: state => {
            return (file_id: string, fileset: LaxyFileSet | null): LaxyFile | undefined => {
                // if the fileset isn't specified we can still retrieve the file object by searching
                // all filesets in the store.
                // TODO: make this more efficient (maybe keep an index of {file_id: file})
                if (fileset == null && state.filesets) {
                    for (const fs in state.filesets) {
                        if (fs) {
                            const file = head(filter(state.filesets[fs].files, (f) => f.id === file_id));
                            if (file) return file;
                        }
                    }
                }
                if (fileset != null) {
                    return head(filter(fileset.files, (f: LaxyFile) => {
                        return f.id === file_id;
                    }));
                }
                return undefined;
            };
        },
    },
    mutations: {
        [SET_USER_PROFILE](state, profile_info: {}) {
            state.user_profile = profile_info;
        },
        [ADD_SAMPLES](state, samples: Sample[]) {
            // if (state.samples.items == undefined)
            state.samples.items.push(...samples);
        },
        [SET_SAMPLES](state, samples: SampleSet) {
            state.samples = samples;
        },
        [SET_SAMPLES_ID](state, id: string) {
            state.samples.id = id;
        },
        [SET_PIPELINE_PARAMS](state, params: any) {
            state.pipelineParams = params;
        },
        [SET_PIPELINE_DESCRIPTION](state, txt: any) {
            state.pipelineParams.description = txt;
        },
        [SET_JOBS](state, jobs: JobsPage) {
            state.jobs = jobs;
        },
        [SET_FILESET](state, fileset: LaxyFileSet) {
            // state.filesets[fileset.id] = fileset; // don't preserve reactivity
            Vue.set(state.filesets, fileset.id, fileset); // reactive
        },
        [SET_VIEWED_JOB](state, job: ComputeJob) {
            state.currentViewedJob = job;
        }
    },
    actions: {
        async [FETCH_USER_PROFILE]({commit, state}) {
            try {
                const response = await WebAPI.getUserProfile();
                const profile_info = pick(response.data,
                    ['full_name', 'username', 'email', 'profile_pic']);
                commit(SET_USER_PROFILE, profile_info);
            } catch (error) {
                console.log(error);
                throw error;
            }
        },
        async [SET_SAMPLES]({commit, state}, samples) {
            const preCommit = cloneDeep(state.samples);
            if (preCommit.id != null && samples.id == null) {
                samples.id = preCommit.id;
            }
            // optimistically commit the state
            commit(SET_SAMPLES, samples);
            const data = {
                name: samples.name,
                samples: samples.items
            };
            try {
                if (samples.id == null) {
                    const response = await WebAPI.fetcher.post('/api/v1/sampleset/', data) as AxiosResponse;
                    // samples.id = response.data.id;
                    // commit(SET_SAMPLES, samples);
                    commit(SET_SAMPLES_ID, response.data.id);
                } else {
                    const response = await WebAPI.fetcher.put(
                        `/api/v1/sampleset/${samples.id}/`, data) as AxiosResponse;
                }
            } catch (error) {
                // rollback to saved copy if server update fails
                commit(SET_SAMPLES, preCommit);
                console.log(error);
            }
        },
        async [SET_PIPELINE_PARAMS]({commit, state}, params: any) {
            commit(SET_PIPELINE_PARAMS, params);
        },
        async [FETCH_JOBS]({commit, state}, pagination = {page: 1, page_size: 10}) {
            try {
                const response = await WebAPI.getJobs(
                    pagination.page,
                    pagination.page_size);
                const jobs: JobsPage = {
                    total: response.data.count,
                    jobs: response.data.results as ComputeJob[]
                };
                // ISO date strings to Javascipt Date objects
                for (const key of ['created_time', 'modified_time', 'completed_time']) {
                    update(jobs, key, function (d_str: string) {
                        return new Date(d_str);
                    });
                }
                commit(SET_JOBS, jobs);
            } catch (error) {
                console.log(error);
                throw error;
            }
        },
        async [FETCH_FILESET]({commit, state}, fileset_id: string) {
            try {
                const response = await WebAPI.getFileSet(fileset_id);
                commit(SET_FILESET, response.data);
            } catch (error) {
                console.log(error);
                throw error;
            }
        },
        async [FETCH_JOB]({commit, state}, job_id: string) {
            try {
                const response = await WebAPI.getJob(job_id);
                commit(SET_VIEWED_JOB, response.data);
            } catch (error) {
                console.log(error);
                throw error;
            }
        },
    },
});
