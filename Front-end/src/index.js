import React, { useRef, useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { SearchOutlined } from '@ant-design/icons';
import {
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined
} from "@ant-design/icons";
import reportWebVitals from './reportWebVitals';
import Highlighter from 'react-highlight-words';
import { Space, Table, Tag, Layout, Menu, Modal, Input, Button } from 'antd';

const { Header, Content, Footer, Sider } = Layout;

const App = () => {
  const menuItems = [
    {
      key: '1',
      icon: <UserOutlined />,
      label: 'Contract Summary' // Change 'nav 1' to 'User'
    },
    {
      key: '2',
      icon: <VideoCameraOutlined />,
      label: 'Vendor Directory' // Change 'nav 2' to 'Camera'
    },
    {
      key: '3',
      icon: <UploadOutlined />,
      label: 'Forcast Reporting' // Change 'nav 3' to 'Upload'
    },
    {
      key: '4',
      icon: <UserOutlined />,
      label: 'Procurement Training' // Change 'nav 4' to 'Profile'
    },

  ];

  const [searchText, setSearchText] = useState('');
  const [searchedColumn, setSearchedColumn] = useState('');
  const searchInput = useRef(null);

  const handleSearch = (selectedKeys, confirm, dataIndex) => {
    confirm();
    setSearchText(selectedKeys[0]);
    setSearchedColumn(dataIndex);
  };

  const handleReset = (clearFilters) => {
    clearFilters();
    setSearchText('');
  };

  const getColumnSearchProps = (dataIndex) => ({
    filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => (
      <div style={{ padding: 8 }} onKeyDown={(e) => e.stopPropagation()}>
        <Input
          ref={searchInput}
          placeholder={`Search ${dataIndex}`}
          value={selectedKeys[0]}
          onChange={(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
          onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
          style={{ marginBottom: 8, display: 'block' }}
        />
        <Space>
          <Button
            type="primary"
            onClick={() => handleSearch(selectedKeys, confirm, dataIndex)}
            icon={<SearchOutlined />}
            size="small"
            style={{ width: 90 }}
          >
            Search
          </Button>
          <Button
            onClick={() => clearFilters && handleReset(clearFilters)}
            size="small"
            style={{ width: 90 }}
          >
            Reset
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => {
              confirm({ closeDropdown: false });
              setSearchText(selectedKeys[0]);
              setSearchedColumn(dataIndex);
            }}
          >
            Filter
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => {
              close();
            }}
          >
            Close
          </Button>
        </Space>
      </div>
    ),
    filterIcon: (filtered) => (
      <SearchOutlined style={{ color: filtered ? '#1677ff' : undefined }} />
    ),
    onFilter: (value, record) =>
      record[dataIndex]
        .toString()
        .toLowerCase()
        .includes(value.toLowerCase()),
    onFilterDropdownOpenChange: (visible) => {
      if (visible) {
        setTimeout(() => searchInput.current?.select(), 100);
      }
    },
    render: (text) =>
      searchedColumn === dataIndex ? (
        <Highlighter
          highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
          searchWords={[searchText]}
          autoEscape
          textToHighlight={text ? text.toString() : ''}
        />
      ) : (
        text
      ),
  });

  const columns = [
    {
      title: 'Vendor Name',
      dataIndex: 'name',
      key: 'name',
      ...getColumnSearchProps('name'),
      sorter: (a, b) => a.name.localeCompare(b.name),
      // sorter: (a, b) => a.name.length - b.name.length,
      sortDirections: ['ascend', 'descend'],
    },
    {
      title: 'Organization Name',
      dataIndex: 'org',
      key: 'org',
      ...getColumnSearchProps('org'),
      sorter: (a, b) => a.org.localeCompare(b.org),
      sortDirections: ['ascend', 'descend'],
    },
    {
      title: 'Contract Details',
      dataIndex: 'contract',
      key: 'contract',
      ...getColumnSearchProps('contract'),
      render: (text) => <a onClick={() => handleClick(text)}>{text}</a>,
    },
    {
      title: 'Contract Status',
      key: 'tags',
      dataIndex: 'tags',
      render: (_, { tags }) => (
        <>

          {tags.map((tag) => {
            let color = tag.length > 5 ? 'geekblue' : 'green';
            if (tag === 'active') {
              color = 'green';
            }
            return (
              <Tag color={color} key={tag}>
                {tag.toUpperCase()}
              </Tag>
            );
          })}
        </>
      ),
    },
    {
      title: 'Certifications',
      dataIndex: 'cert',
      key: 'cert',
    },
    {
      title: 'Availability',
      dataIndex: 'aval',
      key: 'aval',
    },
  ];
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modal1Open, setModal1Open] = useState(false);
  const [resourceId, setResourceId] = useState(null);
  const [ContractData, setContractData] = useState({});

  useEffect(() => {
    if (resourceId) {
      const fetchData = async () => {
        try {
          setLoading(true);
          const response = await fetch(`http://localhost:8080/api/resource/${resourceId}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const json = await response.json();
          console.log(json);
          setContractData(json);
        } catch (error) {
          console.error('There was an error fetching the resource:', error);
          setError(error);
        } finally {
          setLoading(false);
        }
      };
      fetchData();
    }
  }, [resourceId]);

  const handleClick = (text) => {
    setModal1Open(true);
    setResourceId(text); // This will trigger the useEffect above
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8080//api/all_resource/');
        console.log(response);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const json = await response.json();
        console.log(json);
        setData(json);
      } catch (error) {
        console.error('Fetch error:', error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // const resource_id = 30006385;
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       setLoading(true);
  //       console.log(resource_id)
  //       const response = await fetch(`http://localhost:8080/api/resource/${resource_id}`);
  //       console.log(response);
  //       if (!response.ok) {
  //         throw new Error(`HTTP error new! status: ${response.status}`);
  //       }
  //       const json = await response.json();
  //       console.log(json);
  //       // setData(json);
  //     } catch (error) {
  //       console.error('Fetch error new:', error);
  //       setError(error);
  //     } finally {
  //       setLoading(false);
  //     }
  //   };
  //   fetchData();
  // }, []);

  return (
    <Layout>
      <Sider
        breakpoint="lg"
        collapsedWidth="0"
        onBreakpoint={(broken) => {
          console.log(broken);
        }}
        onCollapse={(collapsed, type) => {
          console.log(collapsed, type);
        }}
      >
        <div className="logo" style={{ padding: 16, textAlign: 'center' }}>
          <h1>City of Portland</h1>
        </div>
        <div className="demo-logo-vertical" />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={['2']}
          items={menuItems}
        />
      </Sider>
      <Modal
        title="Contract Information"
        style={{
          top: 0,
          bottom: 0,
          right: 0,
          position: "absolute",
        }}
        width={600}
        open={modal1Open}
        onOk={() => setModal1Open(false)}
        onCancel={() => setModal1Open(false)}
      >
        <div className="contract-container">
          <h1>{ContractData["Vendor Name"]}</h1>
          <div className="status-section">
            <span className="status active">ACTIVE</span>
          </div>
          <div className="details-section">
            <div className="detail">
              <span className="detail-title">Contract Number</span>
              <span className="detail-value">{ContractData["Award Id"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Open Contracting ID</span>
              <span className="detail-value">{ContractData["Open Contracting ID"]}</span>
            </div>
            {/* ... existing details ... */}
            <div className="detail">
              <span className="detail-title">Organization name</span>
              <span className="detail-value">{ContractData["Organization Name"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Tender Start Date</span>
              <span className="detail-value">{ContractData["Tender Start Date"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Tender End Date</span>
              <span className="detail-value">{ContractData["Tender End Date"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Procurement method</span>
              <span className="detail-value">{ContractData["Procurement method"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Procurement method details</span>
              <span className="detail-value">{ContractData["Procurement method details"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Award ID</span>
              <span className="detail-value">{ContractData["Award Id"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Amount</span>
              <span className="detail-value">${ContractData["Amount"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Organization ID</span>
              <span className="detail-value">{ContractData["Award Id"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Award Start Date</span>
              <span className="detail-value">{ContractData["Award Start Date"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Award End Date</span>
              <span className="detail-value">{ContractData["Award End Date"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Award description</span>
              <span className="detail-value">{ContractData["Award Description"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Duration (days)</span>
              <span className="detail-value">{ContractData["Duration"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Project Manager</span>
              <span className="detail-value">{ContractData["Project Manager"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Certification</span>
              <span className="detail-value">{ContractData["Certification"]}</span>
            </div>
            <div className="detail">
              <span className="detail-title">Change Orders</span>
              <span className="detail-value">4</span>
            </div>
          </div>
        </div>
      </Modal>
      <Layout>
        <Header
          style={{
            color: 'white',
            textAlign: 'center',
            padding: 0
          }}
        >
          Procurement Management
        </Header>
        <h3
          style={{
            color: 'black',
            textAlign: 'right',
            padding: 0
          }}>WELCOME GENNIE
        </h3>
        <Content
          style={{
            margin: '24px 16px 0',
          }}
        >
          <Table dataSource={data} columns={columns} />
        </Content>
        <Footer
          style={{
            textAlign: 'center',
          }}
        >
        </Footer>
      </Layout>
    </Layout>
  );
};


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

reportWebVitals();