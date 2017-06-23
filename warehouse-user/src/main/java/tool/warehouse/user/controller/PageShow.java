package tool.warehouse.user.controller;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import tool.warehouse.pojo.User;
import tool.warehouse.user.service.UserService;

@Controller
public class PageShow {
	@Autowired
	private UserService userService;
	@RequestMapping("/")
    public String showIndex(Model model,HttpServletRequest request,HttpServletResponse response){
		User user = userService.getUserByToken(request, response);
		model.addAttribute(user);
   	 return "index";
    }
    @RequestMapping("/{page}")
    public String showPage(@PathVariable String page){
   	 return page;
    }
}
