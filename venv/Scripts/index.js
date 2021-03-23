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

                // 根据第一、二、三个标签页名，获取第一个标签页的内容
                let sheet = excel.Sheets[sheetName];

                // 转换为JSON
                let sheetJson = XLSX.utils.sheet_to_json(sheet);

                // 转换成json后，根据对应的图，转成对应的格式
                if (inputId == 'inputLine') {
                    // 线图

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
//调拨数据表
function getColNameCSdb(sheetJson) {
    let keys1 = [];
    let keys2 = [];
    let keys3 = [];
    let keys4 = [];
    let keys5 = [];
    let keys6 = [];
    let keys7 = [];
    let keys8 = [];
    let arrkey = [];
    for (let key1 in sheetJson[1]){
        keys1.push(sheetJson[1][key1])
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

    arrkey.push(keys2,keys3,keys4,keys5,keys6,keys7,keys8)
    console.log(arrkey)
    return arrkey;

}

//************************************
function getColName(sheetJson) {
    // 遍历json的第一行，获取key
    let keys = [];
    for (let key in sheetJson[0]) {
        keys.push(key)
    }
    return keys;
}


//表格测试
//调拨数据表格
function gettable_DB(sheetJson) {
        let keys = getColName(sheetJson);
        let arrkey = getColNameCSdb(sheetJson);
        console.log(arrkey)
        dataTotable_DB(keys,arrkey);
}

//************************************

function dataTotable_DB(keys,arrkey) {
    $("#d1").innerHTML = arrkey[0][1]
}


// 线图的数据封装及显示



// 线图数据展现



