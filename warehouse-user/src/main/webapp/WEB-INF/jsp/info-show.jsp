<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<body>
	<center>
<br />
<p ><font size="+3">个人信息表</font></p>
<br /><br /><br />
<table border="1" cellspacing="0">
<tr height="40">
<td>　工号　</td>
<td>　　　　　${user.id}　　　　　　</td>
<td>　姓名　</td>
<td>　　　　　${user.name}　　　　　　</td>
<td rowspan="4">　　${user.image}　　　　　　</td>
</tr>
<tr height="40">
<td>　等级　</td>
<td>　　　　${user.status} 　　　　　　　</td>
<td>　姓别　</td>
<td>　　　${user.sex}　　　　　　　　</td>
</tr>
<tr height="40">　
<td>出生日期</td>
<td>　　　　${user.birthday}　　　　　　　</td>
<td>入职时间</td>
<td>　　　　　${user.register}　　　　　　</td>
</tr>
<tr height="40">
<td>手机号</td>
<td>　　　　${user.phone} 　　　　　　　</td>
<td>邮箱</td>
<td>　　　　${user.email}　　　　　　　</td>
</tr>
<tr height="40">
<td>公司名称</td>
<td colspan="4">${user.company}</td>
</tr>
<tr height="40">
<td>工作部门</td>
<td colspan="4">${user.department}</td>
</tr>
<tr>
<td height="40" colspan="5"><center>简介</center></td>
</tr>
<tr height="400" ><td rowspan="2" colspan="5">${user.desc}</td></tr>
</table>
</center>
</body>
</html>