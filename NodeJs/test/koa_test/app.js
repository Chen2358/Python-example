const Koa = require('koa');
const app = new Koa();

app.use(async (ctx, next) => {
	const start = new Date().getTime();
	await next();
	const ms = new Date().getTime() - start;
	ctx.reponse.set('X-Response-Time', `${ms}s`);
});

app.use(async (ctx, next) => {
	var name = ctx.request.query.name || 'world';
	ctx.response.type = 'text/html';
	ctx.response.body = `<h1>Hello, ${name}!</h1>`;
});

module.exports = app;