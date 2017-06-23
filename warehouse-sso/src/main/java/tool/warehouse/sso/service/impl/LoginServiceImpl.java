package tool.warehouse.sso.service.impl;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.security.Principal;
import java.util.Enumeration;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletInputStream;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.common.utils.CookieUtils;
import tool.warehouse.common.utils.JsonUtils;
import tool.warehouse.mapper.UserMapper;
import tool.warehouse.pojo.User;
import tool.warehouse.pojo.UserExample;
import tool.warehouse.pojo.UserExample.Criteria;
import tool.warehouse.sso.component.JedisClient;
import tool.warehouse.sso.service.LoginService;
@Service
public class LoginServiceImpl implements LoginService{
	
	@Autowired
	private UserMapper userMapper;
	@Autowired
	private JedisClient jedisClient;
	
	@Value("${LOGIN_SESSION_KEY}")
	private String LOGIN_SESSION_KEY;
	
	@Value("${LOGIN_EXPIRE}")
	private Integer LOGIN_EXPIRE;
	@Override
	public WarehouseResult Login(String id, String password,HttpServletRequest request,HttpServletResponse response) {
		 User user=null ;
		try{
		UserExample example = new UserExample();
		Criteria criteria = example.createCriteria();
		 criteria.andIdEqualTo(id);
		 List<User> list =userMapper.selectByExample(example);
		 if(list==null||list.size()==0){
			 return WarehouseResult.build(400,"员工号或密码不正确");
		 }
		 user = list.get(0);
		 if(!user.getPassword().equals(DigestUtils.md5DigestAsHex(password.getBytes()))){
	 
			 return WarehouseResult.build(400, "员工号或密码不正确");
		 }
		 }catch(Exception e){
			 e.printStackTrace();
			 return WarehouseResult.build(500, "工程师开小差了");
		 }
		
		//登录成功
		String token = UUID.randomUUID().toString();
		System.out.println(token);
		//把用户信息写入redis
		//key:LONGIN_SESSION:{TOKEN}
		jedisClient.set(LOGIN_SESSION_KEY+":"+token, JsonUtils.objectToJson(user));
		jedisClient.expire(LOGIN_SESSION_KEY+":"+token, LOGIN_EXPIRE);
													
		CookieUtils.setCookie(request, response, "LOGIN", token);
		String json = CookieUtils.getCookieValue(request, "LOGIN",true);
		
		
		System.out.println("send mesg");
		return WarehouseResult.ok(token);
	}
	@Override
	public WarehouseResult getUserByToken(String token) {
		//根据token取用户信息
		String json = jedisClient.get(LOGIN_SESSION_KEY+":"+token);
		//判断是否查询到结果
		if(StringUtils.isBlank(json)){
			return WarehouseResult.build(400, "用户session已经过期");
		}
		
		User user  = JsonUtils.jsonToPojo(json, User.class);
		//更新session的过期时间
		jedisClient.expire(LOGIN_SESSION_KEY+":"+token, LOGIN_EXPIRE);
		return WarehouseResult.ok(user);
	}
	

}
