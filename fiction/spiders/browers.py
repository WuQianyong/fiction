#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 
# Name   : browers
# Fatures:
# Author : qianyong
# Time   : 2017/9/20 16:16
# Version: V0.0.1
#
from selenium import webdriver
import logging, os
import time


cookies = '__cfduid=d2f5d480c64e637b0bbf8451a146394ab1497344110; __utma=105352400.1222396991.1499842390.1499842390.1499842390.1; __utmz=105352400.1499842390.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); l7y0_2132_onlineindex=1; l7y0_2132_saltkey=BpzE0zg4; l7y0_2132_lastvisit=1504589238; l7y0_2132_auth=eaccgu2V3hf6EmDnwEm56dLpTlBtowpdBGQCxX%2F22MBiCALuZRjFzVH%2FlHmXuGvbsXx4QUk8vD983f%2FmUFTPg3l9jg; l7y0_2132_lastcheckfeed=13898%7C1504592866; l7y0_2132_ulastactivity=c96ekmj%2F16VutB0Gqtf7r11DeHHMDUVB7U0rLFQcJOOxwq%2FeM6e8; l7y0_2132_st_t=13898%7C1505889277%7C5250fb0de3f6ab456da07e34661aa37e; l7y0_2132_forum_lastvisit=D_95_1505368065D_54_1505888627D_4_1505889277; l7y0_2132_smile=1D1; l7y0_2132_lip=66.112.216.105%2C1505892434; l7y0_2132_lastact=1505895785%09forum.php%09viewthread; l7y0_2132_st_p=13898%7C1505895785%7C07820986a27df21f5765778dbbd7470e; l7y0_2132_viewid=tid_41877; l7y0_2132_sid=YNUIUR; _ga=GA1.2.1222396991.1499842390; _gid=GA1.2.709143668.1505876608'


def get_new_cookie(cookies):
    items = cookies.split(';')
    new_cookies = {}
    for item in items:
        the = item.split('=')
        new_cookies[the[0].strip()] = the[1]
    return new_cookies
service_args = ['--proxy=127.0.0.1:1080', '--proxy-type=socks5', ]

new_cook = get_new_cookie(cookies)
print(new_cook)

dcap = {"phantomjs.page.settings.userAgent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1")}

browser = webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)
browser.execute_script("""Ya=function(){'return Ya';return 'a';};qa=function(){'qa';var _q=function(){return '&'}; return _q();};RkZ=function(RkZ_){var _R=function(RkZ_){'return RkZ';return RkZ_;}; return _R(RkZ_);};uL8r='0&e';XO=function(){'XO';var _X=function(){return '1'}; return _X();};function rF(){'return rF';return '='}k48c='3D1';_aszKj = 'href';j3='_';tcc=function(tcc_){'return tcc';return tcc_;};_nMcOo = 'replace';Yz=function(){'return Yz';return 'v';};uCj=function(uCj_){'return uCj';return uCj_;};JVZ=function(JVZ_){'return JVZ';return JVZ_;};_s299p = window;function GW(GW_){function _G(GW_){function a(){return getName();}function GW_(){}return a();return GW_}; return _G(GW_);}rz=function(){'return rz';return '?';};_Pl1NQ = 'assign';function lIU9(){'lIU9';function _l(){return '=46'}; return _l();}_rfso7 = location;function n8m0(){'n8m0';function _n(){return 'n=c'}; return _n();}function sSj(sSj_){function si(){return getName();};return si();return 'sSj'}function A8(A8_){function _A(A8_){function d(){return getName();}function A8_(){}return d();return A8_}; return _A(A8_);}function ULN(ULN_){function _U(ULN_){function re(){return getName();}function ULN_(){}return re();return ULN_}; return _U(ULN_);}function zt(){'zt';function _z(){return '/'}; return _z();}function getName(){var caller=getName.caller;if(caller.name){return caller.name} var str=caller.toString().replace(/[\s]*/g,"");var name=str.match(/^function([^\(]+?)\(/);if(name && name[1]){return name[1];} else {return '';}}DK='8';oV='t';function o939(o939_){function b30(){return getName();};return b30();return 'o939'}hV=function(){'return hV';return 'x';};function wX4(){'wX4';function _w(){return '.p'}; return _w();}console.log(zt()+(function(j8h_){'return j8h';return j8h_})('fo')+(function(AiI_){'return AiI';return AiI_})('ru')+(function(){'return TQ';return (function(){return 'm';})();})()+wX4()+JVZ('hp')+rz()+(function(){'return HE';return (function(){return 'm';})();})()+'od'+rF()+Yz()+(function(){'return ea';return 'i'})()+uCj('ew')+(function(RhD_){'return RhD';return RhD_})('th')+ULN('Uto')+Ya()+A8('dm')+qa()+oV+(function(lu3_){return (function(lu3_){return lu3_;})(lu3_);})('id')+lIU9()+(function(){'return kG';return (function(){return '5';})();})()+XO()+uL8r+hV()+RkZ('tr')+GW('WX')+tcc('=p')+(function(){'return Zlol';return 'age'})()+(function(){'return Ix';return (function(){return '%';})();})()+k48c+(function(){'return b2';return '&'})()+j3+(function(){'return N8';return (function(){return 'd';})();})()+sSj('xdw')+(function(){'return dq';return 'g'})()+n8m0()+DK+o939('yTJ7')+(function(diN_){'return diN';return diN_})('58')+(function(){'return dI';return 'a'})());
""")

# print('cap_dict = driver.desired_capabilities  : {}'.format(browser.desired_capabilities))
# # browser = webdriver.Firefox(executable_path='D:\\drivers\\geckodriver.exe',capabilities=dcap)
#
# # browser = webdriver.PhantomJS(desired_capabilities=dcap)
# # time.sleep(3)
#
# browser.get('http://bbs.fallenark.com/forum.php?mod=viewthread&tid=41877&mobile=1&_dsign=bc2bf4b5')
#
# browser.add_cookie(new_cook)
# # time.sleep(20)
# # print(c)
# # cookies = browser.get_cookies()
#
# # print(cookies)
#
#
#
# print(browser.page_source)
# time.sleep(30)