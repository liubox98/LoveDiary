import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://10.10.20.24:8000', // 替换为你的后端地址
});
export default instance;

