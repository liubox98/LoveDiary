import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://liuboo.pythonanywhere.com', // 替换为你的后端地址
});
export default instance;
