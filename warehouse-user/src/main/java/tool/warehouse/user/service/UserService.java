package tool.warehouse.user.service;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import tool.warehouse.pojo.User;

public interface UserService {
	public User getUserByToken(HttpServletRequest request,HttpServletResponse response);
	public void Logout(HttpServletRequest request,HttpServletResponse response);
}
