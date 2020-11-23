console.log("scripted called ")

$(document).on('click','.delete-entry',function(){
	var id = $(this).attr('data-id')
	console.log(id)
 $.ajax({
     type: 'post',
     url: '/music/delete/',
     data: {'id':id},
     success: function(data) {
     	if(data){
     		if (data['data']){
     			console.log("delete success")
     			location.reload();
     		}else{
     			console.log("delete failed")
     			location.reload();
     		}
     	}
     },
     error: function(data) {

     },
     complete: function(data) {

     }
 })
})