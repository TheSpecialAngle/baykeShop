// 获取cookie
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


// axios发送请求
function request(config) {
    const instance = axios.create({
        baseURL: '',
        timeout: 5000,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    });
    

    // 拦截请求
    instance.interceptors.request.use(
        config => {
            // console.log(config)
            return config;
        }, err => {
            console.log(err);
        })
    
    // 拦截响应
    instance.interceptors.response.use(
        res => {
            return res
        }, err => {
            // console.log(err.response.status)
            if (err.response.status == 400){
                data = JSON.stringify(err.response.data)
                alert(data)
            }
            return err.response
        }
    )

    return instance(config);
}