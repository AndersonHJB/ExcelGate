function logout() {
    window.location.href = '/logout';
}

function saveData() {
    const rows = document.querySelectorAll('table tr');
    let sheet_data = [];

    rows.forEach(row => {
        let rowData = [];
        row.querySelectorAll('input').forEach(cell => {
            rowData.push(cell.value);
        });
        sheet_data.push(rowData);
    });

    fetch('/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sheet_data: sheet_data }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("表格已成功更新！");
        } else {
            alert("更新失败！");
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
