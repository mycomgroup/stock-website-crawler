async function test() {
  try {
    const res = await fetch('https://rsshub.app/sina/rollnews/2519');
    const text = await res.text();
    console.log(text.substring(0, 1000));
  } catch (e) {
    console.error(e.message);
  }
}
test();
