package tool.warehouse.user;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import tool.warehouse.pojo.User;
import tool.warehouse.user.service.UserService;

public class LoginInterceptorHandler implements HandlerInterceptor{
	@Autowired
	private UserService userService;
	@Value("${SSO_LOGIN_URL}")
	private String SSO_LOGIN_URL;
	
	
	@Override
	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
			throws Exception {
		User user = userService.getUserByToken(request, response);
		System.out.println(user);
		if(user == null){
			response.sendRedirect(SSO_LOGIN_URL);
			return false;
		}			
			
		return true;
	}

	@Override
	public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,
			ModelAndView modelAndView) throws Exception {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
			throws Exception {
		// TODO Auto-generated method stub
		
	}

}
