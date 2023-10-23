function showToast({message, url, callbackFn, statusCode='S'}){
    backgroundColor = statusCode == 'S' ? "linear-gradient(to left, #00359b, #519d)" : "linear-gradient(to left, #923f62, #921f)";
    Toastify({
        text: message,
        duration: 3000,
        destination: url,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, 
        offset : {
            x : 50,
            y : "2.5em"
        },
        style: {
          background: backgroundColor,
        },
        onClick: () => callbackFn // Callback after click
    }).showToast();
}