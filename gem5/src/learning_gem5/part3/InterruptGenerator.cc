#include "learning_gem5/part3/InterruptGenerator.hh"

#include "base/trace.hh"
#include "debug/Interrupt.hh"

namespace gem5
{

InterruptGenerator::InterruptGenerator(const InterruptGeneratorParams &params) :
    SimObject(params),
    interrupt_pin(params.name + ".interrupt_pin", -1, this),
    interrupt_event([this]{ generate_interrupt(); }, name())
{
    DPRINTF(Interrupt, "Creating InterruptGenerator\n");
    schedule(interrupt_event, curTick() + params.interrupt_latency);
}

Port &
InterruptGenerator::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "interrupt_pin") {
        return interrupt_pin;
    } else {
        return SimObject::getPort(if_name, idx);
    }
}

void
InterruptGenerator::generate_interrupt()
{
    DPRINTF(Interrupt, "Generating interrupt\n");
    interrupt_pin.raise();
}

} // namespace gem5
