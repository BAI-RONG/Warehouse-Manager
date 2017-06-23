<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<body>
	<div>
	<ul class="easyui-tree" id="category"></ul>
	</div>
	<div id="mm" class="easyui-menu" style="width:120px;">
		<div id="remove">删除</div>  
        <div onclick="append()">添加</div>
        <div onclick="rename()">重命名</div>    
    </div>    
  <div id="dialog" class="easyui-dialog" title="添加工具类" style="width:400px;height:200px;" closed="true" cache=false>
  	<form id="add" >
  	<br><br><br>
  		<table align="center">
  		
  			<tr >
  				<td>工具类名 : </td>
  				<td align="center"><input type="text" name="name"></td>
  			</tr>
  			<tr>
  			<td><br></td>
  			</tr>
  			<tr align="center">
  				<td><input type="button" id="verify" value="确定" ></td>
  				<td><input type="button" id="cancel" value="取消" ></td>
  			</tr>
    		</table>  		
  		</form>  	
  </div>    
	<script type="text/javascript">
	var flag;
	$(function(){
		$('#category').tree({
			
			url:'/category/list',
			animate:true,
			method:"POST",
			onContextMenu:function(e,node){
				e.preventDefault();
				$(this).tree('select',node.target);
				$('#mm').menu('show',
						{
							left:e.pageX,
							top:e.pageY
						});
			},
			onAfterEdit:function(node){
				
				$.ajax({
					type:'POST',
					url:'/category/update',
					data:{id:node.id,name:node.text},
					dataType:'json',
					success:function(data){
						if(data.status==200){
						$.messager.show({
							title:'提示信息',
							msg:'修改名字成功!'
						});
						}
					}
				})	
			}
		});	
	
	
		$('#cancel').click(function(){
			$('#dialog').dialog('close'); 
	});	
		
		$('#verify').click(function(){
				if(flag=='add'){
					//1 做前台更新   
					//	(1)获取所选中的节点,也就是父节点
					var node = $('#category').tree('getSelected');
					//  (2)调用追加节点的方法
					
					$('#category').tree('append' , {
						parent:node.target ,
						data:[{
							text: $('#add').find("input[name='name']").val() ,
						}]
					});
					
					//2 后台同步更新 
					$.ajax({
						type:'post' ,
						url:'/category/create' ,
						cache:false , 
						data:{
							id:node.id ,
							name:$('#add').find("input[name='name']").val(),
						} ,
						dataType:'json' ,
						success:function(data){
							//刷新节点 
							var parent = $('#category').tree('getParent' , node.target);
							$('#category').tree('update',{
								target : node.target,
		        				id :  data.data,
							});
							$('#category').tree('reload',parent.target);
							
							$.messager.show({
								title:'提示信息',
								msg:'操作成功!'
							});
						}
					});
					//3 关闭dialog
					$('#add').find("input[name='name']").val('');
					$('#dialog').dialog('close');
				}
		});


	});
		function append(){
		flag="add";
		$('#dialog').dialog('open');
	}
	
	function rename(){
		var node = $('#category').tree('getSelected');
		$('#category').tree('beginEdit',node.target);		
	}

	$('#remove').unbind('click').click(function(){
		var node=$('#category').tree('getSelected');
		var parent=$('#category').tree('getParent',node.target);
		if(node.id<=5) {
			$.messager.alert('提示','该节点不能删除!')
			return false;
		}
		$.messager.confirm('确认','确定删除名为 '+node.text+' 的分类吗？',function(r){
			if(r){
				$.ajax({
     			   type: "POST",
     			   url: '/category/delete',
					data : {id:node.id,parentId:parent.id},
     			   dataType:'json',
     			   success: function(data){
     				   
     				   $.messager.show({'提示':'删除类目成功!'});
     					$('#category').tree("remove",node.target);
     					if(data==false){
     						$('#category').tree("update",{
     							target : parent.target,
		        				children:""
     						})
     					}
     			   },
     			   error: function(){
     				   $.messager.alert('提示','删除失败!');
     			   }
     			});
			}
		});
	})	
	</script>
</body>
</html>