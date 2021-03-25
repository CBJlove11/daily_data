// 数据处理入口
var myDate = new Date()
year = myDate.getFullYear()
month = myDate.getMonth()+1
day = myDate.getDate()
function excelToECharts(obj) {
    excelToData(obj);
}


// 读取Excel转换为json
function excelToData(obj) {
    // 获取input标签的id，用这个来控制显示什么图咯
    let inputId = obj.id;
    // 获取文件对象
    let files = obj.files;
    // 如果有文件
    if (files.length) {
        // 初始化一个FileReader实例
        let reader = new FileReader();
        let file = files[0];
        // 看下文件是不是xls或者xlsx的
        let fullName = file.name;   // 全名
        let filename = fullName.substring(0, fullName.lastIndexOf("."));    // 文件名
        let fixName = fullName.substring(fullName.lastIndexOf("."), fullName.length);   // 后缀名
        // 处理excel表格
        if (fixName == ".xls" || fixName == ".xlsx") {
            reader.onload = function (ev) {
                let data = ev.target.result;
                // 获取到excel
                let excel = XLSX.read(data, {type: 'binary'});
                // 获取第一个标签页名字
                let sheetName = excel.SheetNames[0];
                let sheetName2 = excel.SheetNames[1];
                let sheetName3 = excel.SheetNames[2];
                let sheetName4 = excel.SheetNames[3];
                // 根据第一、二、三个标签页名，获取第一个标签页的内容
                let sheet = excel.Sheets[sheetName];
                let sheet2 = excel.Sheets[sheetName2];
                let sheet3 = excel.Sheets[sheetName3];
                let sheet4 = excel.Sheets[sheetName4];
                // 转换为JSON
                let sheetJson = XLSX.utils.sheet_to_json(sheet);
                let sheetJson2 = XLSX.utils.sheet_to_json(sheet2);
                let sheetJson3 = XLSX.utils.sheet_to_json(sheet3);
                let sheetJson4 = XLSX.utils.sheet_to_json(sheet4);
                // 转换成json后，根据对应的图，转成对应的格式
                if (inputId == 'inputLine') {
                    // 线图
                    gettable_YC(sheetJson,filename);
                    dataToLine_YC(sheetJson,filename);
                    gettable_YCtype(sheetJson2,filename);
                    gettable_YCsx(sheetJson3,filename);
                    dataToLine_YCsx(sheetJson3,filename);
                    gettable_XD(sheetJson4,filename);
                    dataToLine_XD(sheetJson4,filename);
                    gettable_XDtype(sheetJson4,filename);
                }/* else if (inputId == 'inputPie') {
                    // 饼图
                    getPieChartFromJson(sheetJson, filename);
                }*/

            }
        } else {
            alert("起开，只支持excel")
        }
        reader.readAsBinaryString(file);
    }
}

// 通过表格数据的json，获取列名，返回列名的数组

//测试用
//异常数据表
function getColNameYC(sheetJson) {
    let keys1 = [];
    let keys2 = [];
    let keys3 = [];
    let keys4 = [];
    let keys5 = [];
    let keys6 = [];
    let keys7 = [];
    let keys8 = [];
    let keys9 = [];
    let arrkey = [];
    for (let key1 in sheetJson[1]){
        keys1.push(sheetJson[0][key1])
    }
    for (let key2 in sheetJson[1]){
        keys2.push(sheetJson[1][key2])
    }
    for (let key3 in sheetJson[1]){
        keys3.push(sheetJson[2][key3])
    }
    for (let key4 in sheetJson[1]){
        keys4.push(sheetJson[3][key4])
    }
    for (let key5 in sheetJson[1]){
        keys5.push(sheetJson[4][key5])
    }
    for (let key6 in sheetJson[1]){
        keys6.push(sheetJson[5][key6])
    }
    for (let key7 in sheetJson[1]){
        keys7.push(sheetJson[6][key7])
    }
    for (let key8 in sheetJson[1]){
        keys8.push(sheetJson[7][key8])
    }
    for (let key9 in sheetJson[1]){
        keys9.push(sheetJson[8][key9])
    }

    arrkey.push(keys1,keys2,keys3,keys4,keys5,keys6,keys7,keys8,keys9)
    return arrkey;
}
function getColNameYC_type(sheetJson2) {
    let keys1 = [];
    let keys2 = [];
    let keys3 = [];
    let keys4 = [];
    let keys5 = [];
    let keys6 = [];
    let keys7 = [];
    let arrkey = [];
    for (let key1 in sheetJson2[1]){
        keys1.push(sheetJson2[0][key1])
    }
    for (let key2 in sheetJson2[1]){
        keys2.push(sheetJson2[1][key2])
    }
    for (let key3 in sheetJson2[1]){
        keys3.push(sheetJson2[2][key3])
    }
    for (let key4 in sheetJson2[1]){
        keys4.push(sheetJson2[3][key4])
    }
    for (let key5 in sheetJson2[1]){
        keys5.push(sheetJson2[4][key5])
    }
    for (let key6 in sheetJson2[1]){
        keys6.push(sheetJson2[5][key6])
    }
    for (let key7 in sheetJson2[1]){
        keys7.push(sheetJson2[6][key7])
    }
    arrkey.push(keys1,keys2,keys3,keys4,keys5,keys6,keys7)
    return arrkey;
}
//异常处理时效
function getColNameYCsx(sheetJson3) {
    let keys1 = [];
    let keys2 = [];
    let keys3 = [];
    let keys4 = [];
    let keys5 = [];
    let arrkey = [];
    for (let key1 in sheetJson3[1]){
        keys1.push(sheetJson3[0][key1])
    }
    for (let key2 in sheetJson3[1]){
        keys2.push(sheetJson3[1][key2])
    }
    for (let key3 in sheetJson3[1]){
        keys3.push(sheetJson3[2][key3])
    }
    for (let key4 in sheetJson3[1]){
        keys4.push(sheetJson3[3][key4])
    }
    for (let key5 in sheetJson3[1]){
        keys5.push(sheetJson3[4][key5])
    }
    arrkey.push(keys1,keys2,keys3,keys4,keys5)
    return arrkey;
}
//采购下单达成率
function getColNameXD(sheetJson4) {
    let keys1 = [];
    let keys2 = [];
    let keys3 = [];
    let keys4 = [];
    let keys5 = [];
    let keys6 = [];
    let keys7 = [];
    let arrkey = [];
    for (let key1 in sheetJson4[1]){
        keys1.push(sheetJson4[0][key1])
    }
    for (let key2 in sheetJson4[1]){
        keys2.push(sheetJson4[1][key2])
    }
    for (let key3 in sheetJson4[1]){
        keys3.push(sheetJson4[2][key3])
    }
    for (let key4 in sheetJson4[1]){
        keys4.push(sheetJson4[3][key4])
    }
    for (let key5 in sheetJson4[1]){
        keys5.push(sheetJson4[4][key5])
    }
    for (let key6 in sheetJson4[1]){
        keys6.push(sheetJson4[5][key6])
    }
    for (let key7 in sheetJson4[1]){
        keys7.push(sheetJson4[6][key7])
    }
    arrkey.push(keys1,keys2,keys3,keys4,keys5,keys6,keys7)
    return arrkey;
}
//************************************
function getColName(sheetJson) {
    // 遍历json的第一行，获取key
    let keys = [];
    for (let key in sheetJson[0]){
        keys.push(key)
    }
    return keys;
}
function getColName2(sheetJson2) {
    // 遍历json的第一行，获取key
    let keys = [];
    for (let key in sheetJson2[0]){
        keys.push(key)
    }
    return keys;
}
function getColName3(sheetJson3) {
    // 遍历json的第一行，获取key
    let keys = [];
    for (let key in sheetJson3[0]){
        keys.push(key)
    }
    return keys;
}
function getColName4(sheetJson4) {
    // 遍历json的第一行，获取key
    let keys = [];
    for (let key in sheetJson4[0]){
        keys.push(key)
    }
    return keys;
}

//表格测试
//异常数据表格
function gettable_YC(sheetJson) {
        let keys = getColName(sheetJson);
        let arrkey = getColNameYC(sheetJson);
        dataTotable_YC(keys,arrkey);
}
function gettable_YCtype(sheetJson2) {
        let keys = getColName2(sheetJson2);
        let arrkey = getColNameYC_type(sheetJson2);
        dataTotable_YCtype(keys,arrkey);
}
function gettable_YCsx(sheetJson3) {
        let keys = getColName3(sheetJson3);
        let arrkey = getColNameYCsx(sheetJson3);
        dataTotable_YCsx(keys,arrkey);
}
function gettable_XD(sheetJson4) {
        let keys = getColName4(sheetJson4);
        let arrkey = getColNameXD(sheetJson4);
        dataTotable_XD(keys,arrkey);
}
function gettable_XDtype(sheetJson4) {
        let keys = getColName4(sheetJson4);
        let arrkey = getColNameXD(sheetJson4);
        dataTotable_XDtype(keys,arrkey);
}
//************************************

function dataTotable_YC(keys,arrkey) {
    document.getElementById('yc1').innerHTML = arrkey[0][arrkey[0].length-1] + arrkey[1][arrkey[1].length-1] + arrkey[2][arrkey[2].length-1]
    document.getElementById('yc2').innerHTML = arrkey[0][arrkey[0].length-1]
    document.getElementById('yc3').innerHTML = arrkey[1][arrkey[1].length-1]
    document.getElementById('yc4').innerHTML = arrkey[2][arrkey[2].length-1]
    document.getElementById('yc5').innerHTML = arrkey[5][arrkey[5].length-1]
    document.getElementById('yc6').innerHTML = arrkey[6][arrkey[6].length-1]
    document.getElementById('yc7').innerHTML = arrkey[7][arrkey[7].length-1]
    document.getElementById('yc8').innerHTML = (arrkey[4][arrkey[4].length-1]*100).toFixed(2)+'%'
    let db_yc1 = (arrkey[0][arrkey[0].length-1] + arrkey[1][arrkey[0].length-1] + arrkey[2][arrkey[0].length-1]) - (arrkey[0][arrkey[0].length-2] + arrkey[1][arrkey[0].length-2] + arrkey[2][arrkey[0].length-2])
    let db_yc2 = arrkey[0][arrkey[0].length-1] - arrkey[0][arrkey[0].length-2]
    let db_yc3 = arrkey[1][arrkey[1].length-1] - arrkey[1][arrkey[1].length-2]
    let db_yc4 = arrkey[2][arrkey[2].length-1] - arrkey[2][arrkey[2].length-2]
    let db_yc5 = arrkey[5][arrkey[5].length-1] - arrkey[5][arrkey[5].length-2]
    let db_yc6 = arrkey[6][arrkey[6].length-1] - arrkey[6][arrkey[6].length-2]
    let db_yc7 = arrkey[7][arrkey[7].length-1] - arrkey[7][arrkey[7].length-2]
    let db_yc8 = (arrkey[4][arrkey[4].length-1] - arrkey[4][arrkey[4].length-2]).toFixed(3)
    arr = [db_yc1,db_yc2,db_yc3,db_yc4,db_yc5,db_yc6,db_yc7,db_yc8]
    arr_id = ['yc1_1','yc1_2','yc1_3','yc1_4','yc1_5','yc1_6','yc1_7','yc1_8']
    for(i=0;i<=arr.length;i++){
        if(arr[i]>0){
            document.getElementById(arr_id[i]).innerHTML = '+'+arr[i]
            document.getElementById(arr_id[i]).className = 'yc_title_a'
        }
        if(arr[i]<0){
            document.getElementById(arr_id[i]).innerHTML = arr[i]
            document.getElementById(arr_id[i]).className = 'yc_title_b'
        }
        if(arr[i]==0){
            document.getElementById(arr_id[i]).innerHTML = arr[i]
        }
    }
}
function dataTotable_YCtype(keys,arrkey) {
    $("#table_yc thead").append('<tr>\n' +
        '        <th style="text-align: left;padding-left:.5rem;background: #f5f6f7;border-right: .0625rem solid #fff;">日期/类型</th>\n' +
        '        <th>'+arrkey[0][0]+'</th>\n'+
        '        <th>'+arrkey[1][0]+'</th>\n'+
        '        <th>'+arrkey[2][0]+'</th>\n'+
        '        <th>'+arrkey[3][0]+'</th>\n'+
        '        <th>'+arrkey[4][0]+'</th>\n'+
        '        <th>'+arrkey[5][0]+'</th>\n'+
        '</tr>\n')
    $("#table_yc tbody").append('                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[1]+'</td>\n' +
        '                    <td>'+arrkey[0][1]+'</td>\n' +
        '                    <td>'+arrkey[1][1]+'</td>\n' +
        '                    <td>'+arrkey[2][1]+'</td>\n' +
        '                    <td>'+arrkey[3][1]+'</td>\n' +
        '                    <td>'+arrkey[4][1]+'</td>\n' +
        '                    <td>'+arrkey[5][1]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[2]+'</td>\n' +
        '                    <td>'+arrkey[0][2]+'</td>\n' +
        '                    <td>'+arrkey[1][2]+'</td>\n' +
        '                    <td>'+arrkey[2][2]+'</td>\n' +
        '                    <td>'+arrkey[3][2]+'</td>\n' +
        '                    <td>'+arrkey[4][2]+'</td>\n' +
        '                    <td>'+arrkey[5][2]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[3]+'</td>\n' +
        '                    <td>'+arrkey[0][3]+'</td>\n' +
        '                    <td>'+arrkey[1][3]+'</td>\n' +
        '                    <td>'+arrkey[2][3]+'</td>\n' +
        '                    <td>'+arrkey[3][3]+'</td>\n' +
        '                    <td>'+arrkey[4][3]+'</td>\n' +
        '                    <td>'+arrkey[5][3]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[4]+'</td>\n' +
        '                    <td>'+arrkey[0][4]+'</td>\n' +
        '                    <td>'+arrkey[1][4]+'</td>\n' +
        '                    <td>'+arrkey[2][4]+'</td>\n' +
        '                    <td>'+arrkey[3][4]+'</td>\n' +
        '                    <td>'+arrkey[4][4]+'</td>\n' +
        '                    <td>'+arrkey[5][4]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[5]+'</td>\n' +
        '                    <td>'+arrkey[0][5]+'</td>\n' +
        '                    <td>'+arrkey[1][5]+'</td>\n' +
        '                    <td>'+arrkey[2][5]+'</td>\n' +
        '                    <td>'+arrkey[3][5]+'</td>\n' +
        '                    <td>'+arrkey[4][5]+'</td>\n' +
        '                    <td>'+arrkey[5][5]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[6]+'</td>\n' +
        '                    <td>'+arrkey[0][6]+'</td>\n' +
        '                    <td>'+arrkey[1][6]+'</td>\n' +
        '                    <td>'+arrkey[2][6]+'</td>\n' +
        '                    <td>'+arrkey[3][6]+'</td>\n' +
        '                    <td>'+arrkey[4][6]+'</td>\n' +
        '                    <td>'+arrkey[5][6]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[7]+'</td>\n' +
        '                    <td>'+arrkey[0][7]+'</td>\n' +
        '                    <td>'+arrkey[1][7]+'</td>\n' +
        '                    <td>'+arrkey[2][7]+'</td>\n' +
        '                    <td>'+arrkey[3][7]+'</td>\n' +
        '                    <td>'+arrkey[4][7]+'</td>\n' +
        '                    <td>'+arrkey[5][7]+'</td>\n' +
        '                </tr>')

}
function dataTotable_YCsx(keys,arrkey){
    document.getElementById('sx1').innerHTML = arrkey[0][arrkey[0].length-1].toFixed(2)
    document.getElementById('sx2').innerHTML = arrkey[1][arrkey[1].length-1].toFixed(2)
    document.getElementById('sx3').innerHTML = arrkey[2][arrkey[2].length-1].toFixed(2)
    document.getElementById('sx4').innerHTML = arrkey[3][arrkey[3].length-1].toFixed(2)
    document.getElementById('sx5').innerHTML = arrkey[4][arrkey[4].length-1].toFixed(2)
    let db_sx1 = (arrkey[0][arrkey[0].length-1]-arrkey[0][arrkey[0].length-2]).toFixed(2)
    let db_sx2 = (arrkey[1][arrkey[1].length-1]-arrkey[1][arrkey[1].length-2]).toFixed(2)
    let db_sx3 = (arrkey[2][arrkey[2].length-1]-arrkey[2][arrkey[2].length-2]).toFixed(2)
    let db_sx4 = (arrkey[3][arrkey[3].length-1]-arrkey[3][arrkey[3].length-2]).toFixed(2)
    let db_sx5 = (arrkey[4][arrkey[4].length-1]-arrkey[4][arrkey[4].length-2]).toFixed(2)
    arr = [db_sx1,db_sx2,db_sx3,db_sx4,db_sx5]
    arr_id = ['sx1_1','sx1_2','sx1_3','sx1_4','sx1_5']
    for(i=0;i<=arr.length;i++){
        if(arr[i]>0){
            document.getElementById(arr_id[i]).innerHTML = '+'+arr[i]
            document.getElementById(arr_id[i]).className = 'yc_title_a'
        }
        if(arr[i]<0){
            document.getElementById(arr_id[i]).innerHTML = arr[i]
            document.getElementById(arr_id[i]).className = 'yc_title_b'
        }
        if(arr[i]==0){
            document.getElementById(arr_id[i]).innerHTML = arr[i]
        }
    }
}
function dataTotable_XD(keys,arrkey) {
    document.getElementById('xd1').innerHTML = arrkey[0][arrkey[0].length-1]
    document.getElementById('xd2').innerHTML = arrkey[1][arrkey[1].length-1]
    document.getElementById('xd3').innerHTML = (arrkey[6][arrkey[6].length-1]*100).toFixed(2)+'%'
    let db_xd1 = (arrkey[0][arrkey[0].length-1]-arrkey[0][arrkey[0].length-2])
    let db_xd2 = (arrkey[1][arrkey[1].length-1]-arrkey[1][arrkey[1].length-2])
    let db_xd3 = (arrkey[6][arrkey[6].length-1]-arrkey[6][arrkey[6].length-2]).toFixed(2)
    arr = [db_xd1,db_xd2,db_xd3]
    arr_id = ['xd1_1','xd1_2','xd1_3']
    for(i=0;i<=arr.length;i++){
        if(arr[i]>0){
            document.getElementById(arr_id[i]).innerHTML = '+'+arr[i]
            document.getElementById(arr_id[i]).className = 'yc_title_a'
        }
        if(arr[i]<0){
            document.getElementById(arr_id[i]).innerHTML = arr[i]
            document.getElementById(arr_id[i]).className = 'yc_title_b'
        }
        if(arr[i]==0){
            document.getElementById(arr_id[i]).innerHTML = arr[i]
        }
    }
}
function dataTotable_XDtype(keys,arrkey) {
    console.log(keys)
    console.log(arrkey)
    $("#table_xd thead").append(
        '                <tr>\n' +
        '        <th style="text-align: left;padding-left:.5rem;background: #f5f6f7;border-right: .0625rem solid #fff;">日期/类型</th>\n' +
        '        <th>'+arrkey[0][0]+'</th>\n'+
        '        <th>'+arrkey[1][0]+'</th>\n'+
        '        <th>'+arrkey[2][0]+'</th>\n'+
        '        <th>'+arrkey[3][0]+'</th>\n'+
        '        <th>'+arrkey[4][0]+'</th>\n'+
        '        <th>'+arrkey[5][0]+'</th>\n'+
        '                </tr>\n')
    $("#table_xd tbody").append('                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[1]+'</td>\n' +
        '                    <td>'+arrkey[0][1]+'</td>\n' +
        '                    <td>'+arrkey[1][1]+'</td>\n' +
        '                    <td>'+arrkey[2][1]+'</td>\n' +
        '                    <td>'+arrkey[3][1]+'</td>\n' +
        '                    <td>'+arrkey[4][1]+'</td>\n' +
        '                    <td>'+arrkey[5][1]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[2]+'</td>\n' +
        '                    <td>'+arrkey[0][2]+'</td>\n' +
        '                    <td>'+arrkey[1][2]+'</td>\n' +
        '                    <td>'+arrkey[2][2]+'</td>\n' +
        '                    <td>'+arrkey[3][2]+'</td>\n' +
        '                    <td>'+arrkey[4][2]+'</td>\n' +
        '                    <td>'+arrkey[5][2]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[3]+'</td>\n' +
        '                    <td>'+arrkey[0][3]+'</td>\n' +
        '                    <td>'+arrkey[1][3]+'</td>\n' +
        '                    <td>'+arrkey[2][3]+'</td>\n' +
        '                    <td>'+arrkey[3][3]+'</td>\n' +
        '                    <td>'+arrkey[4][3]+'</td>\n' +
        '                    <td>'+arrkey[5][3]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[4]+'</td>\n' +
        '                    <td>'+arrkey[0][4]+'</td>\n' +
        '                    <td>'+arrkey[1][4]+'</td>\n' +
        '                    <td>'+arrkey[2][4]+'</td>\n' +
        '                    <td>'+arrkey[3][4]+'</td>\n' +
        '                    <td>'+arrkey[4][4]+'</td>\n' +
        '                    <td>'+arrkey[5][4]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[5]+'</td>\n' +
        '                    <td>'+arrkey[0][5]+'</td>\n' +
        '                    <td>'+arrkey[1][5]+'</td>\n' +
        '                    <td>'+arrkey[2][5]+'</td>\n' +
        '                    <td>'+arrkey[3][5]+'</td>\n' +
        '                    <td>'+arrkey[4][5]+'</td>\n' +
        '                    <td>'+arrkey[5][5]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[6]+'</td>\n' +
        '                    <td>'+arrkey[0][6]+'</td>\n' +
        '                    <td>'+arrkey[1][6]+'</td>\n' +
        '                    <td>'+arrkey[2][6]+'</td>\n' +
        '                    <td>'+arrkey[3][6]+'</td>\n' +
        '                    <td>'+arrkey[4][6]+'</td>\n' +
        '                    <td>'+arrkey[5][6]+'</td>\n' +
        '                </tr>\n' +
        '                <tr style="background-color: #f5f6f7;">\n' +
        '                    <td class="yc_table_time">'+keys[7]+'</td>\n' +
        '                    <td>'+arrkey[0][7]+'</td>\n' +
        '                    <td>'+arrkey[1][7]+'</td>\n' +
        '                    <td>'+arrkey[2][7]+'</td>\n' +
        '                    <td>'+arrkey[3][7]+'</td>\n' +
        '                    <td>'+arrkey[4][7]+'</td>\n' +
        '                    <td>'+arrkey[5][7]+'</td>\n' +
        '                </tr>')
}

// 线图的数据封装及显示
function dataToLine_YC(sheetJson,filename){
    let keys = getColName(sheetJson);
    let ykeys = getColNameYC(sheetJson);
    let x_data = []
    let y_data1 = []
    let y_data2 = []
    for(i=7;i>0;i--){
        x_data.push(keys[keys.length-i])
        y_data1.push(ykeys[0][keys.length-i]+ykeys[1][keys.length-i]+ykeys[2][keys.length-i])
        y_data2.push(ykeys[4][keys.length-i])
    }
    var yc_1 =echarts.init(document.getElementById('yc_main'))
    var yc_1_option = {
        title:{
            text:'七日异常数据趋势',
             subtext: '单位：条'
        },
        grid:{
            top:'20%',
            bottom:'10%'
        },
        legend:{
            data:['异常总数','异常率'],
            top:'5%'
        },
        xAxis:{
            data:x_data,
            splitLine:{
                show:false
            }
        },
        yAxis:[{
            splitLine:{
                show:false
            }
        },{
            splitLine:{
                show:false
            }
        }],
        series:[{
            type:'bar',
            name:'异常总数',
            itemStyle:{
                color:'#0087ff'
            },
            barWidth:30,
            data:y_data1
        },{
            yAxisIndex: 1,
            type:'line',
            name:'异常率',
            smooth: true,
            data:y_data2,
            label: {
                normal: {
                   show:true,
                    formatter:function (params) {
                    str = params.data;
                    return (str*100).toFixed(2) + '%'
                    },
                    color:'#000'
                }
            }
        }]
    }
    yc_1.setOption(yc_1_option);
}
function dataToLine_YCsx(sheetJson3,filename){
    let keys = getColName3(sheetJson3);
    let ykeys = getColNameYCsx(sheetJson3);
    let x_data = []
    let y_data1 = [] //正常入库
    let y_data2 = [] //退货
    let y_data3 = [] //退款
    let y_data4 = [] //不作处理
    let y_data5 = [] //总时效
    for(i=7;i>0;i--){
        x_data.push(keys[keys.length-i])
        y_data1.push(ykeys[0][keys.length-i])
        y_data2.push(ykeys[1][keys.length-i])
        y_data3.push(ykeys[2][keys.length-i])
        y_data4.push(ykeys[3][keys.length-i])
        y_data5.push(ykeys[4][keys.length-i])
    }
    var yc_2 =echarts.init(document.getElementById('yc_sx'))
    var yc_2_option = {
        title:{
            text:'七日异常处理时效趋势',
             subtext: '单位：小时'
        },
        grid:{
            top:'20%',
            bottom:'10%'
        },
        legend:{
            data:['正常入库','退货','退款','不作处理','总时效'],
            top:'5%'
        },
        xAxis:{
            data:x_data,
            splitLine:{
                show:false
            }
        },
        yAxis:[{
            splitLine:{
                show:false
            }
        }],
        series:[{
            type:'bar',
            name:'正常入库',
            itemStyle:{
                color:'#0087ff'
            },
            barWidth:10,
            data:y_data1
        },{
            type:'bar',
            name:'退货',
            barWidth:10,
            data:y_data2
        }
        ,{
            type:'bar',
            name:'退款',
            barWidth:10,
            data:y_data3
        }
        ,{
            type:'bar',
            name:'不作处理',
            barWidth:10,
            data:y_data4
        }
        ,{
            type:'line',
            name:'总时效',
            smooth: true,
            data:y_data5
        }]
    }
    yc_2.setOption(yc_2_option);
}
function dataToLine_XD(sheetJson4,filename) {
    let keys = getColName4(sheetJson4);
    let ykeys = getColNameXD(sheetJson4);
    let x_data = []
    let y_data1 = [] //采购下单量
    let y_data2 = [] //计划推单量
    let y_data3 = [] //下单率
    for(i=7;i>0;i--){
        x_data.push(keys[keys.length-i])
        y_data1.push(ykeys[0][keys.length-i])
        y_data2.push(ykeys[1][keys.length-i])
        y_data3.push(ykeys[6][keys.length-i])
    }
    var xd_1 =echarts.init(document.getElementById('xd_main'))
    var xd_1_option = {
        title:{
            text:'七日下单数据趋势',
             subtext: '单位：单'
        },
        grid:{
            top:'20%',
            bottom:'10%'
        },
        legend:{
            data:['采购下单量','计划推单量','下单率'],
            top:'5%'
        },
        xAxis:{
            data:x_data,
            splitLine:{
                show:false
            }
        },
        yAxis:[{
            splitLine:{
                show:false
            }
        },{
            splitLine:{
                show:false
            }
        }],
        series:[{
            type:'bar',
            name:'采购下单量',
            itemStyle:{
                color:'#0087ff'
            },
            barWidth:20,
            data:y_data1
        },{
            type:'bar',
            name:'计划推单量',
            itemStyle:{
                color:'#ff4358'
            },
            barWidth:20,
            data:y_data2
        },{
            yAxisIndex: 1,
            type:'line',
            name:'下单率',
            smooth: true,
            data:y_data3,
            label: {
                normal: {
                   show:true,
                    formatter:function (params) {
                    str = params.data;
                    return (str*100).toFixed(2) + '%'
                    },
                    color:'#000'
                }
            }
        }]
    }
    xd_1.setOption(xd_1_option);

}
// 线图数据展现