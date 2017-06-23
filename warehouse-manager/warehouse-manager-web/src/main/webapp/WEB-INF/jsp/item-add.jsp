<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<link href="/js/kindeditor-4.1.10/themes/default/default.css" type="text/css" rel="stylesheet">
<script type="text/javascript" charset="utf-8" src="/js/kindeditor-4.1.10/kindeditor-all-min.js"></script>
<script type="text/javascript" charset="utf-8" src="/js/kindeditor-4.1.10/lang/zh_CN.js"></script>
<div id ="window" > 
	<ul class="easyui-tree" id="cat"></ul>
	</div>
<div>	
	<form id="itemAddForm"  method="post">
	    <table cellpadding="5">
	        <tr>
	            <td>工具类别:</td>
	            <td>
	            	<a href="javascript:void(0)" class="easyui-linkbutton"  id="select">选择类目</a>
	            	<span style='margin-left:10px;' id="title"></span>
	            	<input type="hidden" id="cid" name="cid" style="width: 280px;"></input>
	            </td>
	        </tr>
	        <tr>
	            <td>工具名称:</td>
	            <td><input class="easyui-textbox" type="text" name="name" data-options="required:true" style="width: 280px;"></input></td>
	        </tr>
	        <tr>
	            <td>工具价格:</td>
	            <td><input class="easyui-numberbox" type="text" name="price" data-options="min:1,max:99999999,precision:2,required:true" />
	            </td>
	        </tr>
	        <tr>
	            <td>库存数量:</td>
	            <td><input class="easyui-numberbox" type="text" name="number" data-options="min:1,max:99999999,precision:0,required:true" /></td>
	        </tr>
	         <tr>
	         <td>  公司名称：  </td>
	            <td >
					<select id="company" name="company"  class="easyui-combobox" required=true>
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
				<tr>
	            <td>  所属部门    </td>
<!-- 					0Construction Device Repair 1Automobile Repair 2Appliance Repair 3Computer Repair -->
				<td >
					<select id="department" name="department"   class="easyui-combobox"  validType="checkStatus(this)" required=true value="">
						<option disabled="disabled" selected="selected">---------------------任职部门--------------</option>  
    					<option value=0>Construction Device Repair</option>  
    					<option value=1>Automobile Repair</option>    
    					<option value=2>Appliance Repair</option>  
    					<option value=3>Computer Repair</option>  
  					</select>
				</td>
				</tr>
				<tr>
				<td>　存放地址:　</td>
			<td width="160"><input type="text"  id="id" name="place" style="height:20,width:160" class="easyui-validatebox" required=true  missingMessage="储物柜必须填"  validType="idValid"  invalidMessage="储物柜必须填,不要输入空格" value="" /></td>
	        </tr>
	        <tr>
	            <td>条形码:</td>
	            <td>
	                <input class="easyui-textbox" type="text" name="barcode" data-options="validType:'length[1,30]'" required=true/>
	            </td>
	        </tr>
	        <tr>
	            <td>工具图片:</td>
				<td>
	             <a href="javascript:void(0)" class="easyui-linkbutton picFileUpload" id="img">上传图片</a>
	             
	                         
	            
	            <input type="hidden" name="image" id="image"/>
	            </td>
	 	        </tr>
	 	       <tr>
	 	       <td></td>
	 	       <td id="imageView" ></td>	           
	 	       </tr>
	        <tr>
	            <td>商品描述:</td>
	            <td>
	                <textarea style="width:800px;height:300px;visibility:hidden;" name="desc"></textarea>
	            </td>
	        </tr>
	        
	    </table>
	    
	</form>
	
	<div style="padding:5px">
	    <a href="javascript:void(0)" class="easyui-linkbutton" onclick="submitForm()">提交</a>
	    <a href="javascript:void(0)" class="easyui-linkbutton" onclick="clearForm()">重置</a>
	</div>
	</div>
  
<script type="text/javascript">

var itemAddEditor;
$(function(){

	var kindEditorParams= {
		filePostName  : "uploadFile", //表单提交中file组件的名称
		uploadJson : '/pic/upload', //上传地址
		dir : "image" ,//类型
			allowFileManager : true
	}
	
	$('#img').click(function(){
				KindEditor.editor(kindEditorParams).loadPlugin('multiimage',function(){
			var editor = this;
			editor.plugin.multiImageDialog({
				//点击“全部插入”时执行
				clickFn : function(urlList) {					
					var imgArray = [];
					KindEditor.each(urlList, function(i, data) {
                     
						imgArray.push(data.url);
						//小图片预览
					$("#imageView").append("<td><a id='tmp' href='"+data.url+"'><img src='"+data.url+"' width='80' height='50' /></a></td>");
					});
					//将url用逗号分隔写入到隐藏域中
					$("#image").val(imgArray.join(","));
					editor.hideDialog();
				}
			});
		});
      	});
	
	$('#select').unbind('click').click(function(){
		$(this).after("<span style='margin-left:10px;'></span>");
		
		$('#window').window({
			 resizable:false,
			 minimizable:false,
			 maximizable:false,
			 width:'300',
			    height:"450",
			    modal:true,
			    closed:true,
			    iconCls:'icon-save',
			    title:'选择类目',
			    onOpen : function(){
			    	var win = $(this);
			    	$('#cat').tree({
						
						url:'/category/list',
						animate:true,
						method:"POST",
						onClick:function(node){
							if(node.id<5){
								alert("请选择具体类目!")
								
							}
							$('#cid').val(node.id);
						
					    	$('#title').text(node.text);		
						}
			    	});
			    	
			    },
			
		 }).window('open');
	 });   
 

	
	itemAddEditor=KindEditor.create('textarea[name="desc"]',{
			allowFileManager : true
	})
	
	
		
 });
 
function submitForm(){
	if(!$('#itemAddForm').form('validate')){
		$.messager.alert('提示','表单还未填写完成!');
		return ;
	}
	
	
	
	//将编辑器中的内容同步到隐藏多行文本中
	itemAddEditor.sync();
	
	
	$.ajax({
	   type: "POST",
	   url: "/item/save",
	   data: $("#itemAddForm").serialize(),
	   success: function(){
		   $.messager.alert('提示','新增商品成功!');
// 		   $('#itemAddForm').form('reset');
// 			itemAddEditor.html('');
// 			itemAddEditor.sync();
			location.reload();
			
	   }

	});
}

function clearForm(){
	$('#itemAddForm').form('reset');
	itemAddEditor.html('');
	itemAddEditor.sync();
}

</script>