import React, {useState} from 'react';
import {Button, Cascader, Checkbox, Form, InputNumber} from 'antd';
import Upload from "antd/lib/upload/Upload";
const onFinish = (values) => {
    console.log('Success:', values);
};
const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};

const normFile = (e: any) => {
    console.log('Upload event:', e);
    if (Array.isArray(e)) {
        return e;
    }
    return e?.fileList;
};

function UploadOutlined() {
    return null;
}

const optionLists = [
    {
        value: 'zhejiang',
        label: 'Zhejiang',
        isLeaf: false,
    },
    {
        value: 'jiangsu',
        label: 'Jiangsu',
        isLeaf: false,
    },
];


const Barcode = () => {
    const [options, setOptions] = useState(optionLists);
    const onChange = (value, selectedOptions) => {
        console.log(value, selectedOptions);
    };
    const loadData = (selectedOptions) => {
        const targetOption = selectedOptions[selectedOptions.length - 1];

        // load options lazily
        setTimeout(() => {
            targetOption.children = [
                {
                    label: `${targetOption.label} Dynamic 1`,
                    value: 'dynamic1',
                },
                {
                    label: `${targetOption.label} Dynamic 2`,
                    value: 'dynamic2',
                },
            ];
            setOptions([...options]);
        }, 1000);
    };



    return (
    <Form
        name="basic"
        labelCol={{
            span: 8,
        }}
        wrapperCol={{
            span: 16,
        }}
        style={{
            maxWidth: 600,
        }}
        initialValues={{
            remember: true,
        }}
        layout="vertical"
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
    >
        <Form.Item
            label="검색할 도서관 지역"
            name="username"
            rules={[
                {
                    type: 'array',
                    required: true,
                    message: '도서관 지역을 필수로 선택해야합니다.',
                },
            ]}
        >



        <Cascader options={options} loadData={loadData} onChange={onChange} changeOnSelect />
        </Form.Item>

        <Form.Item
            label="ISBN"
            name="isbn13"
            rules={[
                {
                    required: true,
                    message: '13자리의 ISBN을 입력해주세요',
                },
            ]}
        >
            <InputNumber style={{ width: '100%'}}/>
        </Form.Item>



        <Form.Item
            name="upload"
            label="Upload"
            valuePropName="fileList"
            getValueFromEvent={normFile}
            extra="ISBN13 입력대신 바코드를 추출할 수 있습니다"
        >
            <Upload name="logo" action="/upload.do" listType="picture">
                <Button icon={<UploadOutlined />}>Click to upload</Button>
            </Upload>
        </Form.Item>

        <Form.Item
            name="remember"
            valuePropName="unchecked"
            wrapperCol={{
                offset: 0,
                span: 16,
            }}
        >
            <Checkbox>내 Bookwishlist에 바로 추가</Checkbox>
        </Form.Item>

        <Form.Item
            wrapperCol={{
                offset: 0,
                span: 16,
            }}
        >
            <Button type="primary" htmlType="submit">
                검색!
            </Button>
        </Form.Item>
    </Form>
    )
};

// function callRegionJsonAndAppendToOptions(apiUrl){
//     // 도서관 대분류, 중분류
//     fetch(apiUrl)
//         .then(response => {
//             // HTTP 상태 코드 확인
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(jsonData=> {
//             regionJson = jsonData;
//             //지역코드 - 대분류 추가
//
//             for (const [bigcode, bigValue] of Object.entries(jsonData.big)) {
//                 const bigOption = document.createElement("option");
//                 bigOption.text = bigValue;
//                 bigOption.value = bigcode;
//                 bigRegionSelect.appendChild(bigOption);
//             }
//             bigRegionSelect.addEventListener("change", populateSmallRegion);
//             populateSmallRegion();
//
//         })
//         .catch(error => {
//             // 오류 처리 코드
//             console.error('Fetch error:', error);
//         });
// }
// function populateSmallRegion() {
//     // Clear the current options in the "small" region select box
//     smallRegionSelect.innerHTML = "";
//
//
//     const selectedBigRegion = bigRegionSelect.value;
//
//     if (selectedBigRegion in regionJson.small) {
//         const smallRegionData = regionJson.small[selectedBigRegion];
//         // Populate the "small" region select box based on the selected "big" region
//         for (const [smallcode, smallValue] of Object.entries(smallRegionData)) {
//             const smallOption = document.createElement("option");
//             smallOption.text = smallValue;
//             smallOption.value = smallcode;
//             smallRegionSelect.appendChild(smallOption);
//         }
//     }
// }
export default Barcode;

