console.log('✅ Node.js is working!');
console.log('✅ Version:', process.version);

// Test if we can require the packages
try {
    require('express');
    console.log('✅ Express installed');
} catch (e) {
    console.log('❌ Express not found');
}

try {
    require('dotenv');
    console.log('✅ Dotenv installed');
} catch (e) {
    console.log('❌ Dotenv not found');
}