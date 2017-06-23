<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>

<body>
<div data-options="region:'center',title:''" id="content" class="easyui-layout" fit=true border=false href="">
<div id="mydiv" class="easyui-panel" style="width:400px;height:350px"    fit="true" >
    		<form  method="post">
    				<table>
    					<tr>
    						<td>用户名:</td>
    						<td><input type="text" name="username" class="easyui-validatebox" required=true validType="midLength[2,5]" missingMessage="用户名必填!" invalidMessage="用户名必须在2到5个字符之间!"  value="" /></td>
    					</tr>
    					<tr>
    						<td>密码:</td>
    						<td><input type="password" name="password" class="easyui-validatebox" required=true validType="equalLength[4]" missingMessage="密码必填!" value="" /></td>
    					</tr>
    					<tr>
    						<td>性别:</td>
    						<td>
    							男<input type="radio" checked="checked" name="sex" value="1" />
    							女<input type="radio" name="sex" value="2" />
    						</td>
    					</tr>
    					<tr>
    						<td>年龄:</td>
    						<td><input id="age" type="text"  name="age" value="" /></td>
    					</tr>
    					<tr>
    						<td>出生日期:</td>
    						<td><input id="birthday" style="width:160px;"  type="text" name="birthday" value="" /></td>
    					</tr>
    					<tr>
    						<td>所属城市:</td>
    						<td>
    							<input name="city" class="easyui-combobox" url="UserServlet?method=getCity" valueField="id" textField="name"  value="" />
    						</td>
    					</tr>
    					<tr>
    						<td>薪水:</td>
    						<td><input id="salary" type="text" name="salary" value="" /></td>
    					</tr>
    					<tr>
    						<td>开始时间:</td>
    						<td><input id="startTime" style="width:160px;"  type="text" name="startTime"  value="" /></td>
    					</tr>
    					<tr>
    						<td>结束时间:</td>
    						<td><input id="endTime" style="width:160px;"   type="text" name="endTime"  value="" /></td>
    					</tr>   
    					<tr>
    						<td>个人描述:</td>
    						<td><input type="text" name="description" class="easyui-validatebox" required=true validType="midLength[5,50]" missingMessage="个人描述必填!" invalidMessage="描述必须在5到50个字符之间!"  value="" /></td>
    					</tr> 
    					<tr align="center">
    						<td colspan="2">
    							<a class="easyui-linkbutton">保存</a>
    						</td>
    					</tr>   					 					    					    					    					    					    					    					    					
    				</table>
    		</form>
    	</div> 				
    		
    		
</div>
</body>
</html>