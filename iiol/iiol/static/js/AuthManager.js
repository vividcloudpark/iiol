function tryRefreshToken(apiUrl){
    fetch(apiUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    })
};

function isLogined(apiUrl){
    return new Promise(function(resolve, reject){
        fetch(apiUrl, {
            method: "HEAD",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        })
        .then(response => {
            // HTTP 상태 코드 확인
            if (response.status == 401){
                throw new Error('로그인되지 않았습니다.');
            }

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            resolve(true);
        })
        .catch(error => {
            reject(false);
        });
    });   
}


 function getUserInfo(apiUrl){
    return new Promise(function(resolve, reject){
        fetch(apiUrl, {
            method: "GET",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        })
        .then(response => {
            // HTTP 상태 코드 확인
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status == 401){
                throw new Error('로그인되지 않았습니다.');
            }
            resolve(data);
        })
        .catch(error => {
            // 오류 처리 코드
            reject(error);
        });
    });
}