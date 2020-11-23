

$(document).on('click','.delete-entry',function(){
	var id = $(this).attr('data-id')
	console.log(id)
 $.ajax({
     type: 'post',
     url: '/music/delete/',
     data: {'id':id},
     success: function(data) {
     	location.reload(true);
     	// if(data){
     	// 	if (data['data']){
     	// 		console.log("delete success")
     	// 	}else{
     	// 		console.log("delete failed")
     	// 		location.reload(true);
     	// 	}
     	// }
     },
     error: function(data) {
          location.reload(true);
     },
     complete: function(data) {
          location.reload(true);
     }
 })
})