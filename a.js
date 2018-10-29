const Timer = () => new Promise(resovle => {
   
	setTimeout(() => resovle(12),1000)

})
async function main () {
 
	let data = await Timer()
	console.log(data)

}

main()


