exports.handler = (event, context, callback) => {
    let headers = event.headers;
    headers.KEY = process.env.THUNDERFOREST_KEY;
    callback(null, {
        statusCode: 200,
        body: JSON.stringify(headers),
    })
};
