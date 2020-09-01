const fs = require("fs");
const data = require("./data.json");
var parse = {};

function getTeacher(raw) {
    var re = "";

    raw = raw.split('\n');
    for (var i = 0; i < raw.length - 1; i++) {
        if (i !== 0) re += ", ";
        for (var j = 0; j < raw[i].length; j++) {
            if (raw[i][j] === '\t')
                break;
            re += raw[i][j];
        }
    }
    return re;
}
data.forEach(x => {
    //console.log(x);
    var id = x["科號"]; id = id.replace(/\ /g, "");
    var name = x["課程中文名稱"];
    var credit = x["學分數"];
    var teacher = getTeacher(x["授課教師"]);
    var roomAndTime = x["教室與上課時間"].split('\n');
    var room = ""; var time = "";
    for (var i = 0; i < roomAndTime.length - 1; i++) {
        if (i !== 0) room += ", ", time += ", ";
        room += roomAndTime[i].split('\t')[0];

        time += roomAndTime[i].split('\t')[1];
    }
    parse[id] = {
        "id": id,
        "name": name,
        "credit": credit,
        "time": time,
        "room": room,
        "teacher": teacher
    }
})
fs.writeFileSync('./parse.json', JSON.stringify(parse) , 'UTF-8'); 

