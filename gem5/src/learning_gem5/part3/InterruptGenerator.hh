#ifndef __LEARNING_GEM5_PART3_INTERRUPT_GENERATOR_HH__
#define __LEARNING_GEM5_PART3_INTERRUPT_GENERATOR_HH__

#include "params/InterruptGenerator.hh"
#include "sim/sim_object.hh"
#include "dev/intpin.hh"

namespace gem5
{

class InterruptGenerator : public SimObject
{
  private:
    IntSourcePin<SimObject> interrupt_pin;
    void generate_interrupt();
    EventFunctionWrapper interrupt_event;


  public:
    InterruptGenerator(const InterruptGeneratorParams &params);

    Port &getPort(const std::string &if_name, PortID idx) override;
};

} // namespace gem5

#endif // __LEARNING_GEM5_PART3_INTERRUPT_GENERATOR_HH__
