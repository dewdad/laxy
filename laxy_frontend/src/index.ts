declare function require(path: string): any;

// require('file-loader?name=[name].[ext]!../src/index.html');
import 'vue-material/dist/vue-material.css';
// import 'css/slider.css';

import 'es6-promise';

const numeral = require('numeral');

import axios, {AxiosResponse} from 'axios';

import Vue, {ComponentOptions} from 'vue';
import VueRouter from 'vue-router';

import {WebAPI} from './web-api';

const VueMaterial = require('vue-material');
const VueMoment = require('vue-moment');  // for date formatting

Vue.use(VueRouter);
Vue.use(VueMaterial);
Vue.use(VueMoment);

// sadly not working :/
/*
const VueMarkdown = require('vue-markdown');
Vue.use(VueMarkdown);
Vue.component('vue-markdown', VueMarkdown);
*/

import FrontPage from './components/FrontPage.vue';
import FileBrowser from './components/FileBrowser.vue';
import RNASeqSetup from './components/RNASeqSetup.vue';
import InputDataForm from './components/InputFilesForm.vue';
import ENAFileSelect from './components/ENAFileSelect.vue';
import SampleSet from './components/SampleSet.vue';

Vue.component('input-files-form', InputDataForm);

Vue.filter('numeral_format', function (value: number | string, format: string = '0 a') {
    if (!value) return '';
    return numeral(value).format(format);
});

Vue.filter('deunderscore', function (value: string) {
    if (!value) return '';
    value = value.replace('_', ' ')
    // capitalize first letter
    return value.charAt(0).toUpperCase() + value.slice(1);
});

const router = new VueRouter({
    routes: [
        // { path: '/', redirect: '/rnaseq' },
        {
            path: '/',
            name: 'front',
            component: FrontPage,
        },
        {
            path: '/files',
            name: 'files',
            component: FileBrowser,
        },
        {
            path: '/rnaseq',
            name: 'rnaseq',
            component: RNASeqSetup,
        },
        {
            path: '/enaselect',
            name: 'enaselect',
            component: ENAFileSelect,
        },
        {
            path: '/cart',
            name: 'cart',
            component: SampleSet,
        },
    ],
    // mode: 'history',
});

interface MainApp extends Vue {
    logged_in: boolean;
    user_fullname: string;
    login_form_username: string;
    login_form_password: string;
}

const MainApp = new Vue({
    el: '#app',
    router,
    data() {
        return {
            logged_in: false,
            user_fullname: 'John Monash',
            login_form_username: '',
            login_form_password: '',
        };
    },
    methods: {
        async login() {
            const data = (this.$data as MainApp);
            try {
                const response = await WebAPI.login(data.login_form_username, data.login_form_password);
                ((this.$refs as any).loginMenu as any).close();
                (this as any).become_logged_in();
            } catch (error) {
                throw error;
            }
        },
        become_logged_in() {
            const data = (this.$data as MainApp);
            data.login_form_username = '';
            data.login_form_password = '';
            data.logged_in = true;
            // router.push('rnaseq');
        },
        logout(event) {
            sessionStorage.setItem('accessToken', '');
            WebAPI.logout();
            (this.$data as MainApp).logged_in = false;
            // this.$refs["avatarMenu"].close();
            router.push('/');
        },
        openProfile(event) {
            // this.$refs["avatarMenu"].close();
            router.push('profile');
        },
        toggleLeftSidenav() {
            ((this.$refs as any).leftSidenav as any).toggle();
        },
        open(ref: string) {
            console.log('Opened: ' + ref);
        },
        close(ref: string) {
            console.log('Closed: ' + ref);
        },
    }
}) as ComponentOptions<MainApp>;
