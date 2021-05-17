# Quantum realtime communication (A no-communication theorem study)

Small personal project I'm using to experiment with "quantum realtime communication"

WARNING: This is a failed experiment. I've added `strikethrough` markdown in some parts you should probably ignore. The reason why: https://www.forbes.com/sites/chadorzel/2016/05/04/the-real-reasons-quantum-entanglement-doesnt-allow-faster-than-light-communication

Really interesting read. If you're here you should probably give it a go.

I will still publish it on github in order to have it saved just in case someday we manage to break some of the
barriers exposed in the post. (Plus I had to put in some effort on this)

# Problem

Lets imagine that realtime events from online games are small 100 bits package and you want to transfer it from `computer A` to `computer B` as fast as possible: 
- This event has the size of 100 bits
- Even using really good fiber, we are still limited by the time a bit takes to get from point A to point B
- Also, we may need to do multiple travels if we want to send more bits than the fiber supports

The main problem here is that, because of the time it takes to transfer the package from a point to another, we will never be able to 
have close-to-0ms transfer speed even if we can really transfer things at the speed of light (299792458 m/s) communicating across the globe (america to japan: 8246000m). That would result in `8246000/299792458 = 0,02750569529`. Resulting in a ping of 27ms from the american server to the japanese server. Remember that we are not counting the amount of time it takes to transfer information from your
computer to the country server.

Thats the limitation we have with classical computers: We will probably never be able to transfer data faster than the speed of light.

# Quantum entanglement FTW

What is quantum entanglement? Well, TLDR we have ways to create particles with an entangled state. This entanglement basically works even if theyre really far away (you can consider an infinite distance here), ~~if you flip the state of one of the particles and then measure both of them, they should be the same even though you didnt flip the state of the other particle~~.

So thats it, right? All we need to do is entangle two particles and put one in japan and the other one in america and were good to go.
Well, not really, currently we still have no way to read a quantum state without destroying it. That means entanglement would be lost and all we can do is send one particle from a place to the other, flip the its state and then tell someone to measure it through regular communication. Which means even though we can use entanglement to transfer information faster than light, we actually cant because we still have to keep sending new entangled particles from point A to B.

# Solution
If we define that the event package is 100 bits and the transfer speed from point a to point b is 100 bits/s, we can create a constant flux of particles from point a to point b, storing those particles in buffers with an initial handshake and then starting to to read then at a specific speed. Lets say we can read at as speed of 100 bits/s as well.

With that, we will always have a chain of 100 pairs of entangled qubits available every second (1 in america's buffer, the other one in japan's buffer) and ~~we can flip those bits in order to instantly send information from point A to B~~, the only problem is that the package size is limited to the buffer size, so we can only flip/read 100 bits per second.

If you consider that you only need to send 100bits of information per second in order to makes things work, ~~you will end up having instant data transfer from point A to point B. 0ms of delay.~~

# Scaling 
Because of superposition, a qubit can exist in a superposition of values and therefore you need fewer qubits to represent the same values you would represent with a qubit. If you think that its not that much, n classical bits can take the values of `n^2` while quantum bits can take values of `2^n`. Still think thats not much? When scaling, 63 qubits contain as much classical bits as an Exabyte of data while 63 bits is ~8 bytes.

I dont know how superposition works with the approach im taking in my solution but I'm planning on givint it a try.