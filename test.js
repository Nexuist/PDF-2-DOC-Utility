var guid = (function() {
	var counter = 0;

	return function(prefix) {
		var guid = new Date().getTime().toString(32), i;

		for (i = 0; i < 5; i++) {
			guid += Math.floor(Math.random() * 65535).toString(32);
		}

		return (prefix || 'o_') + guid + (counter++).toString(32);
	};
});

console.log(guid()());
