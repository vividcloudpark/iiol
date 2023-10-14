let regionJson;
const bigRegionSelect = document.getElementById("selectbox-big_region");
const smallRegionSelect = document.getElementById("selectbox-small_region_code");

function callRegionJsonAndAppendToOptions(apiUrl){
    // 도서관 대분류, 중분류 
    fetch(apiUrl)
    .then(response => {
        // HTTP 상태 코드 확인
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(jsonData=> {
        regionJson = jsonData;
        //지역코드 - 대분류 추가

        for (const [bigcode, bigValue] of Object.entries(jsonData.big)) {
            const bigOption = document.createElement("option");
            bigOption.text = bigValue;
            bigOption.value = bigcode;
            bigRegionSelect.appendChild(bigOption);
        }
        bigRegionSelect.addEventListener("change", populateSmallRegion);
        populateSmallRegion();

    })
    .catch(error => {
        // 오류 처리 코드
        console.error('Fetch error:', error);
    });
}
function populateSmallRegion() {
    // Clear the current options in the "small" region select box
    smallRegionSelect.innerHTML = "";


    const selectedBigRegion = bigRegionSelect.value;

    if (selectedBigRegion in regionJson.small) {
        const smallRegionData = regionJson.small[selectedBigRegion];
        // Populate the "small" region select box based on the selected "big" region
        for (const [smallcode, smallValue] of Object.entries(smallRegionData)) {
            const smallOption = document.createElement("option");
            smallOption.text = smallValue;
            smallOption.value = smallcode;
            smallRegionSelect.appendChild(smallOption);
        }
    }
}