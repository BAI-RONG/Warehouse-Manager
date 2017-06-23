package tool.warehouse.sso.service;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import tool.warehouse.common.pojo.WarehouseResult;

public interface LoginService {
	

	WarehouseResult Login(String id, String password, HttpServletRequest request, HttpServletResponse response);
	WarehouseResult getUserByToken(String token);
}
