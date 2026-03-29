package tool.warehouse.sso.service.impl;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import org.aspectj.bridge.Message;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.common.utils.ExceptionUtil;
import tool.warehouse.mapper.UserMapper;
import tool.warehouse.pojo.User;
import tool.warehouse.pojo.UserExample;
import tool.warehouse.pojo.UserExample.Criteria;
import tool.warehouse.sso.service.RegisterService;
@Service
public class registerServiceImpl implements RegisterService {
@Autowired
 private UserMapper userMapper;
	@Override
	public WarehouseResult checkData(String id) {
		UserExample example =  new UserExample();
		Criteria criteria = example.createCriteria();
		criteria.andIdEqualTo(id);
		List<User> list=userMapper.selectByExample(example);
		if(list==null||list.isEmpty()){
			return WarehouseResult.ok(true);
		}
		return WarehouseResult.ok(false);
	}
	@Override
	public WarehouseResult register(User user) {
		try{
			user.setPassword(DigestUtils.md5DigestAsHex(user.getPassword().getBytes()));
				if(user.getDepartment()==4&&user.getStatus()==false){
					return WarehouseResult.build(400, "普通员工不可以选Spare");
				}
				userMapper.insertSelective(user);
		return WarehouseResult.ok();
		}catch(Exception e){
			e.printStackTrace();
			return WarehouseResult.build(500, ExceptionUtil.getStackTrace(e));
		}
	}

}
