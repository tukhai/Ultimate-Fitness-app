# -*- coding: utf-8 -*- 
import json

def dictionary_translation():
	dict_trans = {
		'gallery': {
			'vn': 'Ảnh',
			'en': 'gallery'
		},
		'ADD TO CART': {
			'vn': 'THÊM VÀO GIỎ',
			'en': 'ADD TO CART'
		},
		'watermelon': {
			'vn': 'dưa hấu',
			'en': 'watermelon'
		},
		'Home': {
			'vn': 'Trang Chủ',
			'en': 'Home'
		},
		'About us': {
			'vn': 'Giới thiệu',
			'en': 'About us'
		},
		'Shop': {
			'vn': 'cửa hàng',
			'en': 'Shop'
		},
		'Shop By Calendar': {
			'vn': 'Lịch Đặt Hàng',
			'en': 'Shop By Calendar'
		},
		'Contact us': {
			'vn': 'Liên Hệ',
			'en': 'Contact us'
		},
		'My Cart': {
			'vn': 'Giỏ Hàng',
			'en': 'My Cart'
		},
		'Account Info': {
			'vn': 'Thông Tin Tài Khoản',
			'en': 'Account Info'
		},
		'Address Book': {
			'vn': 'Địa Chỉ Giao Hàng',
			'en': 'Address Book'
		},
		'Orders History': {
			'vn': 'Lịch Sử Giao Hàng',
			'en': 'Orders History'
		},
		'Log Out': {
			'vn': 'Đăng Xuất',
			'en': 'Log Out'
		},
		'Sign In': {
			'vn': 'Đăng Nhập',
			'en': 'Sign In'
		},
		'Register Here': {
			'vn': 'Đăng Ký',
			'en': 'Register Here'
		},
		'Total': {
			'vn': 'Tổng',
			'en': 'Total'
		}
	}

	return json.dumps(dict_trans, ensure_ascii=False).decode('utf8')