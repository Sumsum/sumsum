// in src/posts.js
import React from 'react';
import { List, Datagrid, TextField } from 'admin-on-rest/lib/mui';

export const ProductList = (props) => (
    <List {...props}>
        <Datagrid>
            <TextField source="title" />
            <TextField source="type" />
            <TextField source="vendor" />
        </Datagrid>
    </List>
)
