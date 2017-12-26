function transform(wgLat, wgLng){
    var mgLat = 0, mgLng = 0;
    var rad = 6378245.0;
    var ee = 0.00669342162296594323;

    if (outOfChina(wgLat, wgLng)){
        mgLat = wgLat
        mgLng = wgLng
    } else {
        var dLat = transformLat(wgLng - 105.0, wgLat - 35.0);  
        var dLng = transformLng(wgLng - 105.0, wgLat - 35.0);  
        var radLat = wgLat / 180.0 * Math.PI;  
        var magic = Math.sin(radLat);  
        magic = 1 - ee * magic * magic;  
        var sqrtMagic = Math.sqrt(magic);  
        dLat = (dLat * 180.0) / ((rad * (1 - ee)) / (magic * sqrtMagic) * Math.PI);  
        dLng = (dLng * 180.0) / (rad / sqrtMagic * Math.cos(radLat) * Math.PI);  
        mgLat = wgLat + dLat;  
        mgLng = wgLng + dLng;
    }
    return [mgLat, mgLng]
}

function outOfChina(lat, lng){
    if ( lng < 73.004 || lng > 134.6773){
        return true;
    }
    if ( lat < 18.8293 || lat > 53.3471){
        return true;
    }

    if ((lng > 125.3237 && lng < 136.4173) && (lat > 29.6093 && lat < 43.24)){
        return true;
    }

    if ((lng > 73.3237 && lng < 78.4573) && (lat > 7.53 && lat < 32.33)){
        return true;
    }
    
    if ((lng > 80.3237 && lng < 97.81) && (lat < 28.00)){
        return true;
    }

    if ((lng > 97.81 && lng < 108.02) && (lat < 21.00)){
        return true;
    }

    return false;
}

function transformLat(x, y){
    var ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(Math.abs(x))  
    ret += (20.0 * Math.sin(6.0 * x * Math.PI) + 20.0 * Math.sin(2.0 * x * Math.PI)) * 2.0 / 3.0  
    ret += (20.0 * Math.sin(y * Math.PI) + 40.0 * Math.sin(y / 3.0 * Math.PI)) * 2.0 / 3.0  
    ret += (160.0 * Math.sin(y / 12.0 * Math.PI) + 320 * Math.sin(y * Math.PI / 30.0)) * 2.0 / 3.0  
    return ret  
}

function transformLng(x, y){
    var ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(Math.abs(x))  
    ret += (20.0 * Math.sin(6.0 * x * Math.PI) + 20.0 * Math.sin(2.0 * x * Math.PI)) * 2.0 / 3.0  
    ret += (20.0 * Math.sin(x * Math.PI) + 40.0 * Math.sin(x / 3.0 * Math.PI)) * 2.0 / 3.0  
    ret += (150.0 * Math.sin(x / 12.0 * Math.PI) + 300.0 * Math.sin(x / 30.0 * Math.PI)) * 2.0 / 3.0  
    return ret
}