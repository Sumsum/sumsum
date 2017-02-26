import React from 'react';
import { jsonServerRestClient, simpleRestClient, Admin, Resource } from 'admin-on-rest';
import { ProductList } from './products';


const App = () => (
    <Admin restClient={simpleRestClient('http://localhost:8000/api')}>
        <Resource name="products" list={ProductList} />
    </Admin>
)


export default App
