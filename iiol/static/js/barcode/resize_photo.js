const fileInput = document.getElementById("inputbox-photo");
const canvas = document.getElementById("inputbox-photo-canvas");
const ctx = canvas.getContext('2d');

fileInput.addEventListener('change', function(event){
    const file = event.target.files[0];
    
    const reader = FileReader();
    render.onload = function (e) {
        const img= new Image();
        img.src = e.target.result();
        
        img.onload = function(){
            const maxWidth = 300;
            const maxHeight = 300;

            let width = img.width;
            let height = img.height;

            if (width > maxWidth || height > maxHeight){
                if (width > maxWidth){
                    width = maxWidth;
                    height = Math.round(maxWidth * (img.width/img.height));
                } else {
                    height = maxHeight;
                    width = Math.round(maxHeight * (img.width/img.height));
                }
                
            }

            canvas.width = width;
            canvas.height = height;

            ctx.drawImage(img, 0,0, width, height);

            const resizedImaageData = canvas.toDataUrl('image/jpeg');

            img.src = e.target.result;

        }
    }
    reader.readAsDataUrl(file);
})

const imageForm = document.getElementById('barcode-form');
imageForm.addEventListener('submit', function(event){
    event.preventDefault();
    const formData = new FormData(imageForm);
})