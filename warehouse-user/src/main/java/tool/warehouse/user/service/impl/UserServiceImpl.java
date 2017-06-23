package tool.warehouse.user.service.impl;

import java.io.IOException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.CookieValue;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.common.utils.CookieUtils;
import tool.warehouse.common.utils.HttpClientUtil;
import tool.warehouse.pojo.User;
import tool.warehouse.user.component.JedisClient;
import tool.warehouse.user.service.UserService;
import org.springframework.stereotype.Service;
@Service
public class UserServiceImpl implements UserService{
	@Autowired
	private JedisClient jedisClient;
	@Value("${BASE_SSO_URL}")
	private String BASE_SSO_URL;
	@Value("${USER_TOKEN_SERVICE}")
	private String USER_TOKEN_SERVICE;
	@Value("${SSO_LOGIN_URL}")
	private String SSO_LOGIN_URL;
	String token;
	@Override
	public User getUserByToken(HttpServletRequest request, HttpServletResponse response) {
		try{
			
			 token = CookieUtils.getCookieValue(request, "LOGIN");
			System.out.println(token);
			if(StringUtils.isBlank(token)){
				return null;
			}
			String json = HttpClientUtil.doGet(BASE_SSO_URL+USER_TOKEN_SERVICE+token);
			
			WarehouseResult result = WarehouseResult.format(json);
			if(result.getStatus()!=200){
				return null;
			}
			result = WarehouseResult.formatToPojo(json, User.class);
			User user = (User) result.getData();
			return user;
		}catch(Exception e){
			e.printStackTrace();
		return null;
		}
	}
	@Override
	public void Logout(HttpServletRequest request, HttpServletResponse response) {
		CookieUtils cookie = new CookieUtils();
		cookie.deleteCookie(request, response, "LOGIN");
		jedisClient.del("LOGIN_SESSION"+token);
		 try {
			response.sendRedirect(SSO_LOGIN_URL);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
