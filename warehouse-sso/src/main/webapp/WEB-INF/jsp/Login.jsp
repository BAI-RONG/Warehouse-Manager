<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Insert title here</title>
<jsp:include page="/commons/common-js.jsp"></jsp:include>
</head>
<body>
<form method="post" id="LoginForm" >
<table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td bgcolor="#e5f6cf">&nbsp;</td>
  </tr>
  <tr>
    <td height="608" background="/images/login_03.gif"><table width="862" border="0" align="center" cellpadding="0" cellspacing="0">
      <tr>
        <td height="266" background="/images/login_04.gif">&nbsp;</td>
      </tr>
      <tr>
        <td height="95"><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="424" height="95" background="/images/login_06.gif">&nbsp;</td>
            <td width="183" background="/images/login_07.gif"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="21%" height="30"><div align="center"><span class="STYLE3">工号</span></div></td>
                <td width="79%" height="30"><input type="text" id="id" name="id"  style="height:18px; width:130px; border:solid 1px #cadcb2; font-size:12px; color:#81b432;"></td>
              </tr>
              <tr>
                <td height="30"><div align="center"><span class="STYLE3">密码</span></div></td>
                <td height="30"><input type="password" id="password" name="password"  style="height:18px; width:130px; border:solid 1px #cadcb2; font-size:12px; color:#81b432;"></td>
              </tr>
              <tr>
                <td height="30">&nbsp;</td>
                <td height="30"><input type="button" id="login" value="登录"  onclick="Login.login()">
                				<input type="reset" id="reset" value="重置" /></td>
              </tr>
              	
            </table></td>
            <td width="255" background="/images/login_08.gif">&nbsp;</td>
          </tr>
        </table></td>
      </tr>
      <tr>
        <td height="247" valign="top" background="/images/login_09.gif"><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="22%" height="30">&nbsp;</td>
            <td width="56%">&nbsp;</td>
            <td width="22%">&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td height="30"><table width="100%" border="0" cellspacing="0" cellpadding="0">                   	
                          	
              <tr>
                <td width="44%" height="20">&nbsp;</td>
                <td width="56%" class="STYLE4">	<p>还未注册<a href="/page/register">立即注册</a></p> </td>
              </tr>
            </table></td>
            <td>&nbsp;</td>
          </tr>
        </table></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td bgcolor="#a2d962">&nbsp;</td>
  </tr>
</table>
</form>
<map name="Map"><area shape="rect" coords="3,3,36,19" href="#"><area shape="rect" coords="40,3,78,18" href="#"></map>
</body>
<script type="text/javascript">

	var Login={
			before:function(){
				$("#password").val($.trim($("#password").val()))
				$("#id").val($.trim($("#id").val()))
				if($("#id").val()== ""){
					alert('请填写员工号,不要输入空格')
					$("#id").focus();
					return false;
				}
				if($("#password").val() == ""){
					
					alert('请填写员密码,不要输入空格')
					$("#password").focus();
					return false;
				}
				return true;
			},
			login:function(){
				if(Login.before()){
					
					Login.doSubmit();
					
				}
				return false;
			},
			doSubmit:function(){
				$.post("/user/login",$("#LoginForm").serialize(), function(data){	
					if(data.status == 200){
						msg:"欢迎您登录用户系统"
						location.href = "http://localhost:8081"
					}else{
						msg:"密码或员工号ID不正确，请重新输入"
					}
					});
			}
	};
	
</script>

</html>
