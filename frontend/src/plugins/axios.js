import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://172.23.139.224:5000', // 替换为你的后端地址
});
export default instance;
