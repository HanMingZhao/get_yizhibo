
"use strict";
/**
 * 常用公用方法
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var moment_1 = __importDefault(require("moment"));
var util = {
    //获取几tian之前时间
    timeForMatPreDay: function (num) {
        return moment_1["default"]().add({ "days": 0 - num }).format("YYYY-MM-DD");
    },
    //获取几天之后时间
    timeForMatNextDay: function (num) {
        return moment_1["default"]().add({ "days": num }).format("YYYY-MM-DD");
    },
    //获取几个月之前时间
    timeForMatPreMon: function (num) {
        return moment_1["default"]().add({ "months": num }).format("YYYY-MM-DD");
    },
    //获取几年之前时间
    timeForMatPreYear: function (num) {
        return moment_1["default"]().add({ "years": num }).format("YYYY-MM-DD");
    },
    timeForMatPreStr: function (type, num) {
        var that = this;
        var backtime = "";
        if (type == 'year') {
            backtime = that.timeForMatPreYear(num);
        }
        else if (type == 'month') {
            backtime = that.timeForMatPreMon(num);
        }
        else if (type == 'day') {
            backtime = that.timeForMatPreDay(0 - num);
        }
        return backtime;
    },
    // //获取时间差
    //获取时间差:该方法只能取当前时间及之前时间
    getDateStr: function (preYear, preMonth, preDay) {
        return moment_1["default"]().add({ "years": preYear, "months": preMonth, "days": preDay }).format("YYYY-MM-DD");
    },
    //将标注时间格式转为中文年月日
    getchinesedate: function (str) {
        return moment_1["default"](str).format("YYYY年MM月DD日");
    },
    getUrlParams: function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        // if (r != null) return unescape(r[2]); return null;
        if (r != null)
            return decodeURI(r[2]);
        return null;
    },
    //去除数组重复元素
    uniqueArr: function (arr) {
        var tmp = new Array();
        for (var i in arr) {
            if (tmp.indexOf(arr[i]) == -1) {
                tmp.push(arr[i]);
            }
        }
        return tmp;
    },
    uniqueArr2: function (arr) {
        var ret = [];
        var hash = {};
        for (var i = 0; i < arr.length; i++) {
            var item = arr[i];
            var key = typeof (item) + item;
            if (hash[key] !== 1) {
                ret.push(item);
                hash[key] = 1;
            }
        }
        return ret;
    },
    getstockmarket: function (code) {
        if (code.Length < 3)
            return "sh";
        var one = code.substr(0, 1);
        var three = code.substr(0, 3);
        if (one == "5" || one == "6" || one == "9") {
            return "sh";
        }
        else {
            if (three == "009" || three == "126" || three == "110" || three == "201" || three == "202" || three == "203" || three == "204") {
                return "sh";
            }
            else {
                return "sz";
            }
        }
    },
    formatquteid: function (stockcode, market) {
        if (!stockcode || !market)
            return '';
        var marketcode = '';
        switch (market) {
            case 'SHENZHEN':
                marketcode = 'SZ' + stockcode;
                break;
            case 'SHEN':
                marketcode = 'SZ' + stockcode;
                break;
            case 'SHANGHAI':
                marketcode = 'SH' + stockcode;
                break;
            case 'HU':
                marketcode = 'SH' + stockcode;
                break;
        }
        ;
        return marketcode;
    },
    formatcodeMk: function (stockcode, market) {
        var codeMk = '';
        if (!stockcode || !market)
            return '';
        if (market.indexOf('SHEN') > -1 || market.indexOf('SHENZHEN') > -1) {
            codeMk = stockcode ? stockcode + '2' : '';
        }
        if (market.indexOf('HU') > -1 || market.indexOf('SHANGHAI') > -1) {
            codeMk = stockcode ? stockcode + '1' : '';
        }
        return codeMk;
    },
    formatMarketcode: function (stockcode, market) {
        var codeMk = '';
        if (!stockcode || !market)
            return '';
        if (market.indexOf('SHEN') > -1 || market.indexOf('SHENZHEN') > -1) {
            codeMk = stockcode ? '0.' + stockcode : '';
        }
        if (market.indexOf('HU') > -1 || market.indexOf('SHANGHAI') > -1) {
            codeMk = stockcode ? '1.' + stockcode : '';
        }
        return codeMk;
    },
    //字符串截取
    txtLeft: function (txt, n, needtip) {
        if (txt == null || txt == "") {
            return "-";
        }
        var len = 0;
        for (var i = 0; i < txt.length; i++) {
            if (txt.charCodeAt(i) > 255) {
                len += 2;
            }
            else {
                len++;
            }
            if (len > n + 3) {
                if (needtip) {
                    return '<span title="' + txt + '">' + txt.substring(0, i) + "...</span>";
                }
                else {
                    return txt.substring(0, i) + "..";
                }
                break;
            }
        }
        return txt;
    },
    // 将对象转为params形式的string
    dataToParams: function (data) {
        var arr = [];
        for (var k in data) {
            arr.push(k + "=" + data[k]);
        }
        return arr.join("&");
    },
    // 判断字体的颜色，涨：红；跌：绿；无涨跌：黑
    fontColor: function (val) {
        val = ('' + val).replace('%', '');
        if (val > 0) {
            return 'red';
        }
        else if (val < 0) {
            return 'green';
        }
    },
    // 过滤接口返回回来的时间
    changeDate: function (val) {
        var arr = val.split(' ')[0].split('/');
        arr = arr.map(function (item) { return item >= 10 ? item : '0' + item; });
        return arr.join('-');
    },
    // 判断是否是数值，是数值保留两位小数
    toFixed2: function (val, fixed) {
        if (fixed === void 0) { fixed = 2; }
        if (val === '' || val == '-')
            return '-';
        val = parseFloat(val);
        if (isNaN(val))
            return "-";
        return typeof (val) == "number" ? val.toFixed(fixed) : val;
    },
    numFormat: function (value, fixed, unit) {
        if (fixed === void 0) { fixed = 2; }
        if (unit === void 0) { unit = 'auto'; }
        if (value === '' || value == '-')
            return '-';
        value = parseFloat(value);
        if (isNaN(value))
            return "-";
        fixed = typeof fixed == 'undefined' && 2 || fixed;
        var add = '';
        if (unit == "万") {
            value = value / 10000;
        }
        else if (unit == "亿") {
            value = value / 100000000;
        }
        else if (unit == "%") {
            value = value;
            add = '%';
        }
        else if (unit == "auto") {
            if (Math.abs(value) >= 1000000000000) {
                value = value / 1000000000000;
                add = "万亿";
            }
            else if (Math.abs(value) >= 100000000) {
                value = value / 100000000;
                add = "亿";
            }
            else if (Math.abs(value) >= 10000) {
                value = value / 10000;
                add = "万";
            }
        }
        else {
            value = value;
            add = unit;
        }
        value = value.toFixed(fixed);
        return value + add;
    },
    // 取值范围
    getValRegion: function (minVal, maxVal, fixed) {
        if (fixed === void 0) { fixed = 2; }
        var result = "-";
        if (minVal == null) {
            result = this.numFormat(maxVal, fixed);
        }
        else {
            if (maxVal != null) {
                result = minVal == maxVal ? this.numFormat(minVal, fixed) : this.numFormat(minVal, fixed) + "~" + this.numFormat(maxVal, fixed);
            }
            else {
                result = this.numFormat(minVal, fixed);
            }
        }
        return result;
    },
    dateFormat: function (str, type) {
        if (str === '' || str === undefined || str === null || str === '-') {
            return '-';
        }
        try {
            if (/^\d*$/.test(str)) {
                str = parseInt(str);
            }
            type = !!type ? type : 'YYYY-MM-DD';
            var retDate = new Date(str);
            if (isNaN(retDate))
                retDate = this.parseISO8601(str);
            return moment_1["default"](retDate).format(type);
        }
        catch (err) {
            return '-';
        }
    },
    parseISO8601: function (dateStringInRange) {
        var isoExp = /^\s*(\d{4})-(\d\d)-(\d\d)\s*/, date = new Date(NaN), month, parts = isoExp.exec(dateStringInRange);
        if (parts) {
            month = +parts[2];
            date.setFullYear(parts[1], month - 1, parts[3]);
            if (month != date.getMonth() + 1) {
                date.setTime(NaN);
            }
        }
        return date;
    },
    getQueryString: function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = decodeURI(window.location.search).substr(1).match(reg);
        if (r != null)
            return unescape(r[2]);
        return null;
    },
    Substr: function (str, num) {
        var ss;
        // 声明变量。
        if (str.length > num)
            ss = str.substr(0, num) + "...";
        else {
            ss = str;
        }
        // 获取子字符串。
        return ss; // 返回 "Spain"。
    },
    /*
    *判断值是否非空
    */
    getTextValOrEmpty: function (value) {
        if (value != '' && value != undefined && value != null) {
            return value;
        }
        else {
            return '-';
        }
    },
    getDescribe: function (data, num, fix, divide, abs, arr) {
        if (arr === void 0) { arr = null; }
        try {
            if (data === '' || data === undefined || data === null || data === '-' || isNaN(data)) {
                return '<span>-</span>';
            }
            data = parseFloat(data);
            if (data == 0) {
                return "无变化";
            }
            var retult = '';
            if (!arr) {
                arr = ['上升', '下降'];
            }
            if (!divide) {
                retult = this.numFormat(data, num, fix);
            }
            else {
                num = !!parseFloat(num) ? parseFloat(num) : 2;
                if (abs) {
                    retult = Math.abs((data / parseInt(divide))).toFixed(num) + fix;
                }
                else {
                    retult = (data / parseInt(divide)).toFixed(num) + fix;
                }
            }
            var color = '';
            var desc = '';
            color = !!data ? (data == 0 ? '' : data > 0 ? 'red' : 'green') : '';
            desc = !!data ? (data >= 0 ? arr[0] : arr[1]) : '';
            retult = desc + '<span class="' + color + '">' + retult + '</span>';
            return retult;
        }
        catch (err) {
            return '-';
        }
    },
    getColor: function (data) {
        data = parseFloat(data);
        return !!data ? (data == 0 ? '' : data > 0 ? 'red' : 'green') : '';
    },
    getColorByData: function (data, num, fix, divide) {
        try {
            if (data === '' || data === undefined || data === null || data === '-' || isNaN(data)) {
                return '<span>-</span>';
            }
            data = parseFloat(data);
            var retult = '';
            if (!divide) {
                retult = this.FixAmt(data, num, fix);
            }
            else {
                num = !!parseFloat(num) ? parseFloat(num) : 2;
                retult = (data / parseInt(divide)).toFixed(num) + fix;
            }
            var color = '';
            color = !!data ? (data == 0 ? '' : data > 0 ? 'red' : 'green') : '';
            retult = '<span class="' + color + '">' + retult + '</span>';
            return retult;
        }
        catch (err) {
            return '-';
        }
    },
    /*
    *单位自动换算
    */
    FixAmt: function (str, num, fix, ride) {
        try {
            if (str === '' || str === undefined || str === null || str === '-' || isNaN(str)) {
                return '-';
            }
            var result;
            fix = !!fix ? fix : '';
            num = isNaN(parseFloat(num)) ? 2 : parseFloat(num);
            ride = !!ride ? ride : 1;
            str = parseFloat(str) * parseInt(ride);
            var intStr = Math.abs(parseInt(str));
            if (intStr.toString().length > 12) {
                result = (parseFloat(str) / 1000000000000).toFixed(num) + '万亿' + fix;
            }
            else if (intStr.toString().length > 8) {
                result = (parseFloat(str) / 100000000).toFixed(num) + '亿' + fix;
            }
            else if (intStr.toString().length > 4) {
                result = (parseFloat(str) / 10000).toFixed(num) + '万' + fix;
            }
            else {
                result = parseFloat(str).toFixed(num) + fix;
            }
            // console.log(result)
            return result;
        }
        catch (err) {
            return '-';
        }
    }
};
exports["default"] = util;
