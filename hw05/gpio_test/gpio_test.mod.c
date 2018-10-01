#include <linux/build-salt.h>
#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0xb9a84aab, "module_layout" },
	{ 0xfe990052, "gpio_free" },
	{ 0xc1514a3b, "free_irq" },
	{ 0x9387f7ba, "gpiod_unexport" },
	{ 0xd6b8e852, "request_threaded_irq" },
	{ 0xd6951acf, "gpiod_to_irq" },
	{ 0xcab672b2, "gpiod_set_debounce" },
	{ 0xc845f8bc, "gpiod_direction_input" },
	{ 0x9b50fb82, "gpiod_export" },
	{ 0x807871c6, "gpiod_direction_output_raw" },
	{ 0x47229b5c, "gpio_request" },
	{ 0xefd6cf06, "__aeabi_unwind_cpp_pr0" },
	{ 0x7c32d0f0, "printk" },
	{ 0x2a1e74b1, "gpiod_get_raw_value" },
	{ 0x9600e74c, "gpiod_set_raw_value" },
	{ 0xa6a7973f, "gpio_to_desc" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";


MODULE_INFO(srcversion, "E492055AD6A67314207B049");
