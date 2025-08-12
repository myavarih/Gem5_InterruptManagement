#include "learning_gem5/part3/InterruptBridge.hh"
#include "dev/riscv/hifive.hh"

namespace gem5
{

InterruptBridge::InterruptBridge(const InterruptBridgeParams &params) :
    PlicIntDevice(params),
    interrupt_pin(params.name + ".interrupt_pin", 0, this, params.interrupt_id)
{
}

Port &
InterruptBridge::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "interrupt_pin") {
        return interrupt_pin;
    } else {
        return PlicIntDevice::getPort(if_name, idx);
    }
}

void
InterruptBridge::handle_interrupt(int interrupt_id)
{
    static_cast<HiFiveBase *>(platform)->postPciInt(interrupt_id);
}

void
InterruptBridge::raiseInterruptPin(uint32_t num)
{
    handle_interrupt(num);
}

void
InterruptBridge::lowerInterruptPin(uint32_t num)
{
}

InterruptBridge *
InterruptBridge::create(const InterruptBridgeParams &params)
{
    return new InterruptBridge(params);
}

Tick
InterruptBridge::read(PacketPtr pkt)
{
    return 0;
}

Tick
InterruptBridge::write(PacketPtr pkt)
{
    return 0;
}

} // namespace gem5
