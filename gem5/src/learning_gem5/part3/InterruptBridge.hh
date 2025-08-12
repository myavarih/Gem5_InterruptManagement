#ifndef __LEARNING_GEM5_PART3_INTERRUPT_BRIDGE_HH__
#define __LEARNING_GEM5_PART3_INTERRUPT_BRIDGE_HH__

#include "params/InterruptBridge.hh"
#include "dev/riscv/plic_device.hh"
#include "dev/intpin.hh"

namespace gem5
{

class InterruptBridge : public PlicIntDevice
{
  private:
    IntSinkPin<InterruptBridge> interrupt_pin;
    void handle_interrupt(int interrupt_id);

  public:
    InterruptBridge(const InterruptBridgeParams &params);
    static InterruptBridge *create(const InterruptBridgeParams &params);

    Port &getPort(const std::string &if_name, PortID idx) override;

    Tick read(PacketPtr pkt) override;
    Tick write(PacketPtr pkt) override;

    void raiseInterruptPin(uint32_t num);
    void lowerInterruptPin(uint32_t num);
};

} // namespace gem5

#endif // __LEARNING_GEM5_PART3_INTERRUPT_BRIDGE_HH__
