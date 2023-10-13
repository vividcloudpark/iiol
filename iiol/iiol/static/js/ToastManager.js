function showToast(message, callbackFn){
    Toastify({
        text: message,
        duration: 3000,
        destination: "",
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
          background: "linear-gradient(to left, #00359b, #519d)",
        },
        onClick: () => callbackFn // Callback after click
    }).showToast();
}