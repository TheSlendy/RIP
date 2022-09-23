import './App.css';
import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import IconButton from '@mui/material/IconButton'


function RowMenuCell(props){
    const { api, id } = props;
    const handleDeleteClick = (event) => {
        api.updateRows([{ id, _action: 'delete' }]);
    };
    return(
        <IconButton
            color="inherit"
            size="small"
            aria-label="delete"
            onClick={handleDeleteClick}
        >
            <DeleteIcon fontSize="small" />
        </IconButton>
    )
}


const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 100 },
  { field: 'title', headerName: 'Title', width: 200, editable: true },
  { field: 'status', headerName: 'Status', width: 200 },
  { field: 'description', headerName: 'Description', width: 200, editable: true },
  { field: 'delete', headerName: 'Delete', width: 100, sortable: false, disableColumnMenu: true, disableRecorder: true,
  filterable: false, renderCell: RowMenuCell, headerAlign: 'center', align: 'center' }
];

const rows = [
  { "id": 1, "title": 'Snow', "status": 'Done', "description": "None" },
];


function App() {
    const [list, setList] = React.useState(rows);

    const [status, setStatus] = React.useState('');
    const [title, setTitle] = React.useState('');
    const [description, setDescription] = React.useState('');

    const [isError, setError] = React.useState(false)
    const [helper, setHelper] = React.useState('')

    const handleChangeTitle = (event) => {
        setHelper('')
        setError(false);
        setTitle(event.target.value);
    };
    const handleChangeDescription = (event) => {
        setDescription(event.target.value);
    };
    const handleChangeStatus = (event) => {
        setStatus(event.target.value);
    };

    const onButtonClick = (event) => {
        if(title != ''){
            for(let i = 0; i < list.length; i++){
                if(list[i].title === title){
                    setError(true);
                    setHelper('Title must be unique');
                    return;
                }

            }
            const newRows = list.concat({"id": list[list.length - 1].id + 1, "title": title,
            "status": status, "description": description});
            setList(newRows);
        }
        else {
            setError(true);
            setHelper('Title must be filled');
        }
    };

    return (
    <div>
        <div class="todo">
            <b>Todo List</b>
        </div>
        <Box sx={{my: 2, textAlign: "center"}}>
            <TextField
                required
                helperText={helper}
                error={isError}
                id="outlined-required"
                label="Title"
                style = {{width: 200}}
                value={title}
                onChange={handleChangeTitle}
            />
            <TextField
                style = {{width: 200}}
                id="outlined-basic"
                label="Description"
                variant="outlined"
                value={description}
                onChange={handleChangeDescription}
            />
            <FormControl sx={{width: 100}}>
                <InputLabel id="demo-simple-select-label">Status</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={status}
                    label="Status"
                    onChange={handleChangeStatus}
                >
                    <MenuItem value={'Done'}>Done</MenuItem>
                    <MenuItem value={'Not Done'}>Not Done</MenuItem>
                </Select>
            </FormControl>
            <Button onClick={onButtonClick} variant="outlined" sx={{width:100, height:56}}>Add</Button>
        </Box>
      <DataGrid
        rows={list}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        autoHeight
        experimentalFeatures={{ newEditingApi: true }}
      />
    </div>
    );
}

export default App;
