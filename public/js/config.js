const TIME_MAPPING = {
  '1': '0810-0900',
  '2': '0910-1000',
  '3': '1010-1100',
  '4': '1110-1200',
  '5': '1210-1300',
  '6': '1310-1400',
  '7': '1410-1500',
  '8': '1510-1600',
  '9': '1610-1700',
  'a': '1710-1800',
  'b': '1810-1900',
  'c': '1910-2000',
  'd': '2010-2100',
  'e': '2110-2200'
}
const ORDERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e'];
const DAYS = ['M', 'T', 'W', 'R', 'F', 'S'];

const GRADE = {
  "全部開課單位": "[1-9]",
  "大一": "[1]",
  "大二": "[2]",
  "大三": "[3]",
  "大四": "[4]",
  "學士班": "[1-4]",
  "碩士、博士班": "[5-6]",
  "博士班": "[7-9]"
}
const COURSE_TYPE = ['選修', '必修', '通識'];
const BERIEF_CODE = [];
const FIND_COURSE_RESULT_LIMIT = 75;

const YEAR = '110', SEMESTER = '10';

const APP_URL = `${location.protocol}//${location.host}${location.pathname}`;
const YS = YEAR + SEMESTER;
const DEV = location.hostname === '127.0.0.1';

// const OAUTH_CLIENT_ID = "797878714864-n37e7s68t1lqa5qr6fl7k7ubdie68cff.apps.googleusercontent.com";
// const OAUTH_ORIGIN = DEV ? "http://127.0.0.1:5001" : "https://us-central1-nctuwu-9d0d4.cloudfunctions.net";


const firebaseConfig = {
  apiKey: "AIzaSyAe4jl_P_KqIwxLB5Wsp_XLauEGcE5lbEk",
  authDomain: "utaipeiwu.firebaseapp.com",
  databaseURL: "https://utaipeiwu-default-rtdb.firebaseio.com/",
  projectId: "utaipeiwu",
  storageBucket: "utaipeiwu.appspot.com",
  messagingSenderId: "608286255819",
  appId: "1:608286255819:web:7bd81c571aaa500f08c94e",
  measurementId: "G-N9VH9FQYS2"
};
