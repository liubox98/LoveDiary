import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://47.100.41.212:8100', // 替换为你的后端地址
});
export default instance;
