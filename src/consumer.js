const sleep = (ms) => {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
};

const handler = async (event) => {
  for (const rec of event.Records) {
    const body = JSON.parse(rec.body);
    console.log(`delay second - ${body.delaySecond}`);
    await sleep(1000);
  }
};

module.exports = { handler };
