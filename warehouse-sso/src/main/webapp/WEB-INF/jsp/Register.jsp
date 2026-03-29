<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>员工信息注册</title>
<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">    
	<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
	<meta http-equiv="description" content="This is my page">
	<link href="/js/kindeditor-4.1.10/themes/default/default.css" type="text/css" rel="stylesheet">
<script type="text/javascript" charset="utf-8" src="/js/kindeditor-4.1.10/kindeditor-all-min.js"></script>
<script type="text/javascript" charset="utf-8" src="/js/kindeditor-4.1.10/lang/zh_CN.js"></script>
<jsp:include page="/commons/common-js.jsp"></jsp:include>

</head>

<body>
<p style="float:right; padding-right:100px">
已注册:
<a href="/page/login" >直接登录</a>
</p>
	<center>
<br />
<p ><font size="+1">个人信息表</font></p>
<form id="regForm" method="post" >
<table border="1" cellspacing="0">
<tr height="20">
<td>　工号　</td>
<td width="160"><input type="text"  id="id" name="id" style="height:20,width:160" class="easyui-validatebox" required=true  missingMessage="员工号必须填"  validType="idValid"  invalidMessage="员工号必须填,不要输入空格" value="" /></td>
<td>　姓名　</td>
<td width="160"><input type="text" id="name" name="name" style="width:160" class="easyui-validatebox" required=true  missingMessage="姓名必须填，不要输入空格"  validType="midLength[1,50]"  invalidMessage="用户名必须填且不能超过50字" value="" /></td>
<td rowspan="4">
 			<input type="hidden" name="imag" /> 
              <a href="javascript:void(0)" class="onePicUpload">点击上传图片</a>
</td>
</tr>
<tr height="20">
<td>　等级　</td>
<td width="160"><select id="status" name="status" style="width:100%" class="easyui-combobox" required=true>
		<option disabled="disabled" value="等级" selected="selected">-----选择等级-----</option>
	    <option value=false>普通员工</option>  
    	<option value=true>专家</option>      
  </select></td>  

<td>　姓别　</td>
<td width="160">
<select id="sex" name="sex" style="width:100%" class="easyui-combobox">
	<option disabled="disabled" value="性别" selected="selected">-------性别-------</option>  
    <option value=true>女</option>  
    <option value=false>男</option>    
  </select>
  
</td>　　

</tr>
<tr height="20">　
<td>  出生日期    </td>
<td width="160"><input id="birthday" style="width:100%,height=100%"  type="text" name="birthday" value="" class="easyui-datebox"/></td>
<td>  入职时间    </td>
<td width="160"><input id="register" style="width:160px;"  type="text" name="register" value="" class="easyui-datebox" /></td>
</tr>
<tr height="20">
<td>  手机号    </td>
<td width="160"><input id="phone" name="phone" value=""  class="easyui-validatebox" validType="phoneRex"></td>
<td>  邮箱       </td>
<td width="160"><input id="email" name="email" value=""  class="easyui-validatebox" validType="email"></td>
</tr>
<tr height="20">
<!-- 0总公司 1ALI 2BAI 3CUR 4DUIS 5EWQR 6FAUD 7GRAN 8HUA -->
<td >  公司名称     </td>
<td width="500" colspan="4">
<select id="company" name="company" style="width:100%;" class="easyui-combobox" required=true>
	<option disabled="disabled"  selected="selected">---------------------公司名称-------------</option>  
    <option value="0">总公司</option>  
    <option value="1">ALI</option>    
    <option value="2">BAI</option>  
    <option value="3">CUR</option>
    <option value="4">DUIS</option>  
    <option value="5">EWQR</option>
    <option value="6">FAUD</option>  
    <option value="7">GRAN</option>
    <option value="8">HUA</option>  
  </select>
</td>
</tr>
<tr height="20">
<td>  工作部门    </td>
<!-- 0Construction Device Repair 1Automobile Repair 2Appliance Repair 3Computer Repair -->
<td colspan="4" width="500">
<select id="department" name="department"  style="width:500px;" class="easyui-combobox"  validType="checkStatus(this)" required=true value="">
	<option disabled="disabled" selected="selected">---------------------任职部门--------------</option>  
    <option value=0>Construction Device Repair</option>  
    <option value=1>Automobile Repair</option>    
    <option value=2>Appliance Repair</option>  
    <option value=3>Computer Repair</option>  
    <option value=4 >Spare(expert only)</option>
  </select>
</td>
</tr>
<tr>
<td height="20" colspan="5"><center>简介</center></td>
</tr>
<tr  rowspan="4"><td rowspan="2" colspan="5"  width="540"><textarea style="height:250px;width:540px" name="content"></textarea></td></tr>
</table>
<ul>
<li>密码:<input type="password" name ="password" id="password" class="easyui-validatebox" required=true validType="pwdValid[1,50]" missingMessage="密码必填!不要输入空格" value="" />
&nbsp&nbsp验证密码:<input type="password" id="check" class="easyui-validatebox" validType="check" required=true  missingMessage="验证密码必填!不要输入空格"
 invalidMessage="填写与密码不一致，请重新填写！" value="" /></li>

</ul>
<div style="padding:5px">
	    <input type="button"  id="registsubmit" value="立即注册" tabindex="8"   onclick="REGISTER.reg();"/>
	</div>
</form>
	
</center>
</body>
<script type="text/javascript">

$(function(){
	TT.initOnePicUpload();

	// 自定义的校验器
	$.extend($.fn.validatebox.defaults.rules, {   
			midLength: {   
			 			validator: function(value, param){   
			 				if($("#name").val($.trim($("#name").val()))==""){
			 					msg:"不要输入空格"
			 					$("#name").focus()
			 				}
    								return value.length >= param[0] && value.length <= param[1];    
					},   
					message: ''  
			} ,
			idValid:{
				validator: function(){   
	 				if($("#id").val($.trim($("#id").val()))==""){
	 					msg:"不要输入空格"
	 					$("#id").focus()
	 					return false
	 				}
	 				return true
	 				}
			},
			pwdValid:{
				validator: function(value, param){   
	 				if($("#password").val($.trim($("#password").val()))==""){
	 					msg:"不要输入空格"
	 					$("#password").focus()
	 					return false
	 				}
							return value.length >= param[0] && value.length <= param[1];    
			},   
				
			},
			check :{
				
					validator : function(){
						if($("#check").val($.trim($("#check").val()))==""){
		 					msg:"不要输入空格"
		 					$("#check").focus()
		 					return false
		 				}
						
						if ($("#password").val() != $("#check").val()) {
							return false;
						}return true;
						message:''
											
					}
									
			},
			
		
						
			phoneRex : {
				
				validator: function(value){
					
					$('#phone').val($.trim($('#phone').val()));
				var rex=/^1[3-8]+\d{9}$/;
				//var rex=/^(([0\+]\d{2,3}-)?(0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/;
				//区号：前面一个0，后面跟2-3位数字 ： 0\d{2,3}
				//电话号码：7-8位数字： \d{7,8
				//分机号：一般都是3位数字： \d{3,}
				 //这样连接起来就是验证电话的正则表达式了：/^((0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/		 
				var rex2=/^((0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/;
				if(rex.test(value)||rex2.test(value))
				{
				  // alert('t'+value);
				  return true;
				}else
				{
				 //alert('false '+value);
				   return false;
				}
				  
				},
				message: '请输入正确电话或手机格式'
			},
			
		
		});
	
	
		
	$('#birthday,#register').datebox({
			editable:false
	})

})



	var REGISTER={
	beforeSubmit:function() {
		
		
		
		$.ajax({
        	url : "/user/check/"+escape($("#id").val()),
        	success : function(data) {
        		
        	
        		if (!data.data) {
        			
        			$.messager.show({
    					title:'提示信息' , 
    					msg:'注册失败,改员工号已被注册，请登录!'
    				});
    				
        			alert("注册失败，改员工号已被注册，请登录");
        			return false;		
        		}else{
        			     			
        		
        			REGISTER.doSubmit();
        			}
        		
        	}
			
		}
		);	
		
	      	
},
doSubmit:function() {
	
	$.post("/user/register",$("#regForm").serialize(), function(data){
			alert("coming")	
		if(data.status == 200){
			alert('用户注册成功，请登录！');
			REGISTER.login();
		} else if(data.status == 400) {
			
			msg:'普通用户不能选择Spare!'
			alert("普通用户不能选择Spare");
		}else{
			alert("注册失败");
		}
	});
},
		login:function() {
			 location.href = "/page/login";
			 return false;
		},
		reg:function() {
			if(!$('#regForm').form('validate')){
				$.messager.show({
					title:'提示信息' , 
					msg:'验证没有通过,不能提交表单!'
				});
				
				return false ;		//当表单验证不通过的时候 必须要return false 
			}else{
				this.beforeSubmit();
		
		}		
						
		}
	};
</script>

</html>