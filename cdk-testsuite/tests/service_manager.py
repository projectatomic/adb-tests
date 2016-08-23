#!/usr/bin/python

from avocado import Test
from avocado import main
from avocado.utils import process
import re, os, imp, vagrant, pexpect, re ,time
import subprocess
vsm = imp.load_source('vsm', '../Logic/vsm.py')


class service_manager(Test):
	def setUp(self):
		self.log.info("setup")
		self.vagrant_VAGRANTFILE_DIR=self.params.get('vagrant_VAGRANTFILE_DIR')
		self.vagrant_PLUGIN_PATH=self.params.get('vagrant_PLUGIN_PATH')	
		self.service = self.params.get('service', default='')
		self.vagrant_PROVIDER = self.params.get('vagrant_PROVIDER', default='hyperv')
		os.chdir(self.vagrant_VAGRANTFILE_DIR)
		self.v = vagrant.Vagrant(self.vagrant_VAGRANTFILE_DIR)

	def test_cdkbox_version(self):		
		output = vsm.vsm_box_info(self.vagrant_VAGRANTFILE_DIR, "version", "--script-readable")	
		print output
		self.assertIn("Container Development Kit (CDK)",out.stdout)
		
	def  test_vsm_box_ip(self):
		output = vsm.vsm_box_info(self.vagrant_VAGRANTFILE_DIR, "ip", "")
		ip = output.stdout
		ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',ip)
		print ips[0]
		self.assertTrue(ips[0])
		
	def test_env_info_docker(self):

		output = vsm.vsm_env_info(self.vagrant_VAGRANTFILE_DIR, "docker","--script-readable")
		print output.stdout
		self.assertIn("DOCKER_HOST" and "DOCKER_CERT_PATH" and "DOCKER_TLS_VERIFY" and "DOCKER_API_VERSION" , output.stdout)
		

	def test_env_info_openshift(self):
		output = vsm.vsm_env_info(self.vagrant_VAGRANTFILE_DIR, "openshift","--script-readable")
		print output.stdout
		self.assertIn("OPENSHIFT_URL" and "OPENSHIFT_WEB_CONSOLE" and "DOCKER_REGISTRY" , output.stdout)
		

	def test_vsm_status_of_docker_service_running(self):
		output = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "status", "docker")
		print output.stdout
		self.assertIn("docker - running",output.stdout)
		

	def test_vsm_status_openshift_service_running(self):
		output = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "status", "openshift")
		print output.stdout
		self.assertIn("openshift - running",output.stdout)
		
		
	
	def test_stop_openshift_service_start_again(self):
		vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "stop", "openshift")
		output = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "status", "openshift")
		print output.stdout
		if "openshift - stopped" in output.stdout:
			restart = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "start", "openshift")
			time.sleep(20)
			output = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "status", "openshift")
			
			self.assertIn("openshift - running" , output.stdout)
			
		else:
			self.assertTrue("openshift - running" , output.stdout)
		
	def test_stop_docker_service_start_again(self):
		vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "stop", "docker")
		output = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "status", "docker")
		print output.stdout
		if "docker - stopped" in output.stdout:
			restart = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "start", "docker")
			time.sleep(20)
			output = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "status", "")
			if "docker - running" and "openshift - running" in output.stdout:
				pass
			else:
				restart = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "restart", "docker")
				time.sleep(30)
				output = vsm.vsm_service_handling(self.vagrant_VAGRANTFILE_DIR, "status", "")
				
				self.assertIn("docker - running" and "openshift - running" , output.stdout)
				
			
		else:
			self.assertIn("docker - running" , output.stdout)
		

   	

   	def test_docker_version_host(self):
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "docker",'', "docker version")
   		print out,err
   		self.assertIn('Client' and 'Server',out)
   		

   	def test_docker_images_host(self):
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "docker", '',"docker images")
   		print out,err
   		self.assertIn('registry.access.redhat.com',out)
   		

   	def test_docker_ps(self):
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "docker",'', "docker ps")
   		print out,err
   		self.assertIn('openshift',out)
   		
   	def test_docker_pull(self):
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "docker", '',"docker pull tutum/hello-world")
   		print out,err
   		self.assertIn('Status: Downloaded newer image for docker.io/tutum/hello-world:latest',out)
   		
   	
   	def test_docker_rmi(self):
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "docker",'', "docker rmi tutum/hello-world")
   		print out,err
   		self.assertIn('Deleted',out)
   		

   	def test_openshift_from_host_version(self):

   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "openshift",'', "oc version")
   		print out,err
   		self.assertIn('oc v1.2.1',out)
   	
   	def test_openshift_from_host_version(self):

   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "openshift", '',"oc version")
   		print out,err
   		self.assertIn('oc v1.2.1',out)
   		
   	def test_openshift_login_host(self):
   		(out,err)=vsm.box_ip(self.vagrant_VAGRANTFILE_DIR,'ip')
   		out=out.replace('ESC[0m','')
   		ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',out)
		print ips[0]
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "openshift",'', "oc login " +ips[0]+" --username=openshift-dev "+" --password=devel  --insecure-skip-tls-verify")
   		print out,err
   		self.assertIn('Login successful',out)
   		
   		
   	
   	def test_openshift_newproject_host(self):
   		(out,err)=vsm.box_ip(self.vagrant_VAGRANTFILE_DIR,'ip')
   		out=out.replace('ESC[0m','')
   		ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',out)
		print ips[0]
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "openshift",'', "oc login " +ips[0]+" --username=openshift-dev "+" --password=devel  --insecure-skip-tls-verify;oc new-project test-project")
   		print out,err
		self.assertIn('test-project',out)  		
   		
   		
   	def test_install_cli_with_versions(self):
   		(out,err)=vsm.instll_cli(self.vagrant_VAGRANTFILE_DIR, "docker",'--cli-version 1.12.1', "docker version")
   		print out,err
   		self.assertIn('1.12.1',out)
