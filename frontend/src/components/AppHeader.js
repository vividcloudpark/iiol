import React, { useState } from 'react';
import "./AppLayout.scss"

import { BarcodeOutlined, ReadOutlined, MailOutlined, IdcardOutlined } from '@ant-design/icons';
import { Menu } from 'antd';

const items = [
  {
    label: 'IIOL',
    key: 'IIOL',
  },
  {
    label: '바코드로 찾아보기',
    key: 'barcode',
    icon: <BarcodeOutlined />,
  },
  {
    label: 'MyBookwishlist',
    key: 'mmybookwishlist',
    icon: <ReadOutlined />,
  },
  {
    label: '내 계정',
    key: 'SubMenu',
    icon: <IdcardOutlined />,
    children: [
      {
        type: 'group',
        label: '정보',
        children: [
          {
            label: '내 정보 변경',
            key: 'setting:1',
          },
          {
            label: 'Option 2',
            key: 'setting:2',
          },
        ],
      },
     
    ],
  },
];

export default function AppHeader() {
  const [current, setCurrent] = useState('IIOL');

  const onClick = (e) => {
    console.log('click ', e);
    setCurrent(e.key);
  };

  
  return (
    <div className="header">
      <Menu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} theme="dark" />
    </div>
  )
}
